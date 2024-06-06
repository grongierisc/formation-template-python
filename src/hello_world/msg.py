from grongier.pex import Message
from dataclasses import dataclass

@dataclass
class MyResponse(Message):
    string_value: str
    var: dict = None

@dataclass
class MyRequest(Message):
    string_value: str
    var: dict = None