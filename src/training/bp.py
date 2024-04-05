from grongier.pex import BusinessProcess

from msg import TrainingMessage

class TrainingProcess(BusinessProcess):

    def on_message(self, request:TrainingMessage):
        
        response = self.send_request_sync('Python.WriteTrainingFileOperation', request)

        if response.to_db:
            self.send_request_sync('Python.TrainingPostgresOperation', request)

