from grongier.pex import BusinessProcess

from msg import (TrainingRequest,TrainingResponse
                 ,SelectTrainingRequest,SelectTrainingResponse
                 ,SelectDataFrameRequest,SelectDataFrameResponse
                 ,SelectDataFramePickleRequest,SelectDataFramePickleResponse,
                 FormationRequest)


from obj import Training, Formation

class Router(BusinessProcess):

    def on_request(self, request):
        return None
    
    def route(self, request:FormationRequest):
        # transform FormationRequest to TrainingRequest
        msg = TrainingRequest(
                training=Training(
                    name=request.formation.nom,
                    room=request.formation.salle
                )
            )
        # send TrainingRequest to FileOperation and IrisOperation
        self.send_request_sync('Python.FileOperation',msg)
        # save response in response
        response = self.send_request_sync('Python.IrisOperation',msg)
        # print response
        self.log_info(str(response.toto))
        # passe plat de la reponse
        return response
    
class RouterPostgres(BusinessProcess):

    def on_request(self, request):
        msg = SelectTrainingRequest()
        self.route(msg)
        msg = SelectDataFrameRequest()
        self.route_df(msg)
        msg = SelectDataFramePickleRequest()
        self.route_df_pickle(msg)
    
    def route(self, request:SelectTrainingRequest):
        # get all training from postgres
        rsp = self.send_request_sync('Python.PostgresOperation',request)
        # log_info all response
        for t in rsp.trainings:
            self.log_info(str(t))

    def route_df(self, request:SelectDataFrameRequest):
        # get all training from postgres
        rsp = self.send_request_sync('Python.PostgresOperation',request)
        # log_info all response
        for t in rsp.trainings:
            self.log_info(str(t))

    def route_df_pickle(self, request:SelectDataFramePickleRequest):
        # get all training from postgres
        rsp = self.send_request_sync('Python.PostgresOperation',request)
        # log_info all response
        for t in rsp.trainings:
            self.log_info(str(t))