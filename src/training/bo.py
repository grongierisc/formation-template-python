from grongier.pex import BusinessOperation
from msg import TrainingMessage,TrainingAck, TrainingOrmMessage, Training

import os
import random

import psycopg2

from sqlalchemy import create_engine
import pandas as pd

import iris

class IrisTrainingOperation(BusinessOperation):
    def on_training_request(self, request : TrainingMessage):
        if request.verbe == 'POST':
            return self.post_training(request.training)
        elif request.verbe == 'GET':
            return self.get_training(request.training)
        elif request.verbe == 'PUT':
            return self.put_training(request.training)
        elif request.verbe == 'DELETE':
            return self.delete_training(request.training)
        else:
            return TrainingAck(to_db=False)
        
    def delete_training(self, training):
        if iris.cls("Python.Training")._ExistsId(training.id)==1:
            iris.cls("Python.Training")._DeleteId(training.id)

    def put_training(self, training):
        if iris.cls("Python.Training")._ExistsId(training.id)==1:
            training_obj = iris.cls("Python.Training")._OpenId(training.id)
            training_obj.Name = training.name
            training_obj.Room = training.room
            training_obj._Save()
            return TrainingMessage(training=Training(id=training_obj._Id() ,name=training_obj.Name, room=training_obj.Room))
        else:
            return TrainingAck(to_db=False)
    
    def post_training(self, training):
        training_obj = iris.cls("Python.Training")._New()
        training_obj.Name = training.name
        training_obj.Room = training.room
        training_obj._Save()
        return TrainingMessage(training=Training(id=training_obj._Id() ,name=training_obj.Name, room=training_obj.Room))

    def get_training(self, training):
        if hasattr(training, 'id') and training.id == '':
            rs = iris.sql.exec("SELECT ID,Name,Room FROM Python.Training")
            training_list = []
            for training_obj in rs:
                training_list.append(Training(id=training_obj[0], name=training_obj[1], room=training_obj[2]))
            rsp = TrainingMessage(training=Training())
            rsp.training_list = training_list
            return rsp
        if iris.cls("Python.Training")._ExistsId(training.id)==1:
            training_obj = iris.cls("Python.Training")._OpenId(training.id)
            return TrainingMessage(training=
                                   Training(id=training_obj._Id() 
                                            ,name=training_obj.Name, 
                                            room=training_obj.Room))


class ReadTrainingFromIrisOperation(BusinessOperation):
    def on_training_request(self, request: TrainingMessage):
        if iris.cls("Python.Training")._ExistsId(request.training.id)==1:
            self.log_info(f"Training with id {request.training.id} exists")
            training = iris.cls("Python.Training")._OpenId(request.training.id)
            self.log_info(f"Training name : {training.Name} and room : {training.Room}")
            return TrainingMessage(training=Training(id=training._Id(), name=training.Name, room=training.Room))
       
        return None

class WriteTrainingFileOperation(BusinessOperation):
    def on_init(self):
        if not hasattr(self, 'filename'):
            self.filename = 'training.txt'
        if not hasattr(self, 'path'):
            self.path = '/tmp'

    def on_training_request(self, request : TrainingMessage) -> TrainingAck:
        full_path = os.path.join(self.path, self.filename)
        with open(full_path, 'a') as f:
            f.write(f'training name :  {request.training.name} and room : {request.training.room}\n')
        # choose True or False randomly
        return TrainingAck(to_db=random.randint(0, 1) == 1)

class TrainingPostgresOperation(BusinessOperation):

    def on_init(self):
        self.connection = None

        self.host = 'db'
        self.database = 'DemoData'
        self.user = 'DemoData'
        self.password = 'DemoData'

        self.connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

        self.engine = create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}/{self.database}')

    def on_tear_down(self):
        self.connection.close()

    def on_training_request(self, request : TrainingMessage):
        with self.connection.cursor() as cursor:
            cursor.execute("""insert into formation (name, room) values (%s, %s)""", 
                           (request.training.name, request.training.room)
                        )
            self.connection.commit()

    def on_orm_request(self, request : TrainingOrmMessage):
        # create a dataframe based on TrainingOrmMessage
        df = pd.DataFrame([request.training.__dict__])
        # remove the id column from the dataframe
        df = df.drop(columns='id')
        # write the dataframe to the database
        df.to_sql('formation', self.engine, if_exists='append', index=False)
