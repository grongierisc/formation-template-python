from grongier.pex import BusinessOperation

from hello_world.msg import MyResponse, MyRequest

from training.msg import EmptyMessage

class HelloWorldBO(BusinessOperation):

    def on_init(self):
        if not hasattr(self, "url"):
            self.url = "default"

    # numero 1
    def on_message(self, request):
        self.log_info("numero 1")
    
    # numero 4
    def hello_say_hello2(self, request: MyRequest):
        self.log_info(f"numero 4")
        
        simple_string = "toto"

        return MyResponse(self.url)
