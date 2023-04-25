from grongier.pex import BusinessOperation

# import the kafka producer
from kafka import KafkaProducer

from msg_kafka import KafkaMessage

class KafkaOperation(BusinessOperation):

    def on_init(self):
        # init the kafka producer
        self.producer = KafkaProducer(bootstrap_servers='kafka:29092')

    def on_message(self, request:KafkaMessage):
        # send the message to the kafka topic
        self.producer.send(request.topic, request.value.encode('utf-8'))
        self.producer.flush()
