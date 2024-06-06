from grongier.pex import BusinessProcess

from training.msg import FormationRequest, FormationResponse, EmptyMessage

import iris

class FormationBP(BusinessProcess):

    def transform_wrapper(self,transform_name,  input):
        self.log_info(f"Transforming {transform_name}")
        my_ref = iris.ref(None)
        iris.cls(transform_name).Transform(input,my_ref)
        return my_ref.value

    def on_formation_request(self, request: FormationRequest):

        self.log_info(f"Formation {request.id} - {request.nom} - {request.salle}")
        input = iris.cls("Formation.Training")._New()
        input.Name = request.nom
        input.Room = request.salle

        output = self.transform_wrapper("Formation.DT.TrainingToFormation", input)

        self.log_info(f"TrainingToFormation: {output.Nom} - {output.Salle}")

        self.send_request_sync("Python.FormationFileBO", FormationRequest(
            id=request.id,
            nom=output.Nom,
            salle=output.Salle
        ))

