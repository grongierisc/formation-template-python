from grongier.pex import BusinessService,Message

import os

from msg import FormationRequest
from obj import Formation

class ServiceCSV(BusinessService):

    path = "/irisdev/app/misc"

    def get_adapter_type():
        """
        Name of the registred adaptor
        """
        return "Ens.InboundAdapter"
    
    def on_init(self):
        """
        Called when the service is created
        """
        if hasattr(self,'path'):
            self.path="/irisdev/app/misc"

        if hasattr(self,'archive'):
            self.archive="/irisdev/app/misc/archive"

    def on_process_input(self,request):
        # 1. real all csv file in path
        # 2. for each file, call cast the line to a message
        # 3. create a FormationRequest
        # 4. send the message to the BusinessProcess
        # 5. move the file to archive

        # 1. real all csv file in path
        for file in os.listdir(self.path):
            if file.endswith(".csv"):
                # 2. for each file, call cast the line to a message
                with open(os.path.join(self.path,file)) as f:
                    # first line is the header
                    f.readline()
                    for line in f:
                        # 3. create a FormationRequest
                        # 4. send the message to the BusinessProcess
                        msg  = FormationRequest(
                            formation=Formation(
                                nom=line.split(";")[1],
                                salle=line.split(";")[2]
                            )
                        )
                        self.send_request_sync('Python.Router',msg)
                # 5. move the file to archive
                os.rename(os.path.join(self.path,file),os.path.join(self.archive,file))

class FlaskService(BusinessService):

    def on_process_input(self,msg):
        return self.send_request_sync('Python.Router',msg)

    def on_tear_down(self):
        self.log_info("on tear down")
        print("on tear down")

