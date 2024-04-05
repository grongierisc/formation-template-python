from grongier.pex import BusinessService
from msg import TrainingMessage, Training

import os


class TrainingRestService(BusinessService):
    def dispatch_process(self, message: TrainingMessage):
        self.send_request_sync('Python.TrainingProcess', message)

    def dispatch_message(self, message: TrainingMessage):
        return self.send_request_sync('Python.IrisTrainingOperation', message)


class TrainingPoolingService(BusinessService):

    def on_init(self):
        self.in_path = '/irisdev/app/misc/in'
        self.out_path = '/irisdev/app/misc/out'
        self.filename = 'formation.csv'
    
    def get_adapter_type():
        return "Ens.InboundAdapter"
    
    def on_process_input(self, message_input):
        full_in_path = os.path.join(self.in_path, self.filename)

        try:
            with open(full_in_path, 'r') as f:
                lines = f.readlines()
                # skip first line
                for line in lines[1:]:
                    fields = line.split(';')
                    training = TrainingMessage(
                        training=Training(
                            id=fields[0],
                            name=fields[1],
                            room=fields[2]
                            )
                        )
                    self.send_request_sync('Python.TrainingProcess', training)
            # move file to out directory
            full_out_path = os.path.join(self.out_path, self.filename)
            os.rename(full_in_path, full_out_path)
        except FileNotFoundError:
            pass
