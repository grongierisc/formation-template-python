from grongier.pex import Message
from dataclasses import dataclass

@dataclass
class HelloWorldMessage(Message):
    message: str