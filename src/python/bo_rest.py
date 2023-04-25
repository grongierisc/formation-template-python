from grongier.pex import BusinessOperation

import requests

from msg import FormationRequest
from obj import Formation

class RestOperation(BusinessOperation):

    def on_init(self):

        if not hasattr(self,'url'):
            self.url = "http://127.0.0.1:5000/formation" 
            #https://mockbin.org/bin/echo

    def post_formation(self,request:'iris.Ens.StringRequest'):

        formation = Formation("toto","titi")
        # send the message to the rest service
        my_paylaod = formation.__dict__

        r=requests.post(self.url, json=my_paylaod, timeout=20)

        #r.raise_for_status()

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