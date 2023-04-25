from grongier.pex import BusinessOperation

class MyOperation(BusinessOperation):

    def on_message(self, request):
        self.log_info('Hello World !!!')