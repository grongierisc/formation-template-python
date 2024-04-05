from grongier.pex import BusinessOperation
from msg import HelloWorldMessage

class HelloWorldBO(BusinessOperation):

    def on_message(self, request):
        self.log_info("Hello World BO received a message")
        return HelloWorldMessage(message="Hello World")

    def hello_by_names(self, request: 'iris.Ens.StringRequest'):
        self.log_info(f"hello : {request.StringValue}")