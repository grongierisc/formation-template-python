from grongier.pex import BusinessOperation

import requests

from msg import FormationRequest
from obj import Formation

class RestOperation(BusinessOperation):

    def on_init(self):

        if not hasattr(self,'url'):
            self.url = "http://localhost:5000/formation"

    def post_formation(self,request:FormationRequest):

        # send the message to the rest service
        my_paylaod = request.formation.__dict__

        r = requests.post(self.url, json=my_paylaod)

        r.raise_for_status()



if __name__ == '__main__':
    bo = RestOperation()
    bo.on_init()
    msg = FormationRequest(
        formation=Formation(
            nom="Python",
            salle="A"
        )
    )
    bo.post_formation(msg)

