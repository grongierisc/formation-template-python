# Creer une business operation qui prend en entree le message FormationRequest
# Et ecrit dans un fichier txt avec le format suivant :
# {id} - {nom} - {salle}

from grongier.pex import BusinessOperation
from training.msg import FormationRequest, FormationResponse, HttpRequest, HttpResponse

import requests

import random

import os

class FormationFileBO(BusinessOperation):

    def on_init(self):
        if not hasattr(self, "filename"):
            self.filename = "formations.txt"
        if not hasattr(self, "path"):
            self.path = "/tmp/"
    
    def on_formations(self, request: FormationRequest):
        self.log_info(f"Formation {request.id} - {request.nom} - {request.salle}")
        
        with open(os.path.join(self.path, self.filename), "a") as file:
            file.write(f"{request.id} - {request.nom} - {request.salle}\n")

        # simulate a random validation
        return FormationResponse(valide=random.choice([True, False]))

class HttpBO(BusinessOperation):
    def on_init(self):
        if not hasattr(self, "url"):
            self.url = "default"
    
    def exchange(self, request: HttpRequest):
        self.log_info(f"Requesting {request.url}")
        
        response = requests.request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            data=request.body,
            timeout=5
        )
        
        return HttpResponse(
            status_code=response.status_code,
            headers=response.headers,
            body=response.text
        )
        

    
