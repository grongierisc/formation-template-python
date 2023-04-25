from grongier.pex import BusinessOperation

from msg import (TrainingRequest,TrainingResponse
                 ,SelectTrainingRequest,SelectTrainingResponse
                 ,SelectDataFrameRequest,SelectDataFrameResponse
                 ,SelectDataFramePickleRequest,SelectDataFramePickleResponse)

from obj import Training

import iris
import psycopg2

import pandas as pd
from sqlalchemy import create_engine

import random

class FileOperation(BusinessOperation):

    def on_message(self, request):
        return None
    
    def insert_to_file(self, request:TrainingRequest):
        # insert to file
        with open("/tmp/training.txt", "a") as myfile:
            myfile.write(request.training.name + ":" + request.training.room + "\n")


class IrisOperation(BusinessOperation):

    def on_message(self, request):
        return None

    def insert_to_table(self, request:TrainingRequest):
        # insert to table iris.training
        sql = """
        insert into iris.training (name, room) values (?,?)
        """
        iris.sql.exec(sql,request.training.name,request.training.room)
        
        # get a random number between 0 and 100
        r = random.random()
        rsp = TrainingResponse(toto=False)
        # if r < 0.5, raise an exception
        if r < 0.5:
            rsp = TrainingResponse(toto=True)

        return rsp

class PostgresOperation(BusinessOperation):

    def on_init(self):
        self.conn = psycopg2.connect("postgresql://DemoData:DemoData@db:5432/DemoData")

    def insert_into_pg(self,request:TrainingRequest):
        
        # insert to table formation
        sql = """
        insert into formation (name, room) values (%s,%s)
        """
        with self.conn.cursor() as cur:
            cur.execute(sql,(request.training.name,request.training.room))
        self.conn.commit()

    def on_tear_down(self):
        self.conn.close()

    def select_from_pg(self,request:SelectTrainingRequest):
        sql = """
        select * from formation
        """
        with self.conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            trainings = []
            for row in rows:
                trainings.append(Training(name=row[0],room=row[1]))
            rsp = SelectTrainingResponse(trainings=trainings)
        return rsp

    def select_to_dataframe(self,request:SelectDataFrameRequest):
        sql = """
        select * from formation
        """
        engine = create_engine('postgresql://DemoData:DemoData@db:5432/DemoData')
        df = pd.read_sql_query(sql,con=engine)

        rsp = SelectDataFrameResponse(trainings=df)
        return rsp
    
    def select_to_dataframe_pickle(self,request:SelectDataFramePickleRequest):
        sql = """
        select * from formation
        """
        engine = create_engine('postgresql://DemoData:DemoData@db:5432/DemoData')
        df = pd.read_sql_query(sql,con=engine) 
        rsp = SelectDataFramePickleResponse(trainings=df)
        return rsp

