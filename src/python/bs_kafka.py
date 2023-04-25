from grongier.pex import BusinessService

from kafka import KafkaConsumer

from msg_kafka import KafkaMessage

class KafkaService(BusinessService):
    
    def get_adapter_type():
        """
        Name of the registred adaptor
        """
        return "Ens.InboundAdapter"

    def on_init(self):
        # init the kafka consumer
        self.consumer = KafkaConsumer('formation', bootstrap_servers='kafka:29092')

    def on_process_input(self,request):
        # read one message from the kafka topic
        msg = next(self.consumer)
        self.log_info("message received from kafka: %s" % msg.value)

    def OnTearDown(self):
        # close the kafka consumer
        self.log_info("close the kafka consumer")
        self.consumer.close()