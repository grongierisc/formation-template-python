from grongier.pex import Message
from dataclasses import dataclass

@dataclass
class KafkaMessage(Message):
    topic:str = None
    value:str = None


