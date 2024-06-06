from grongier.pex import Message, PickleMessage
from dataclasses import dataclass

# Create a formation message with parameters
# id: int
# nom: str
# salle: str
@dataclass
class FormationRequest(Message):
    id: int = None
    nom: str = None
    salle: str = None

# Create a response message with parameters
@dataclass
class FormationResponse(Message):
    valide: bool = None

@dataclass
class EmptyMessage(Message):
    pass

@dataclass
class HttpRequest(Message):
    url: str = None
    method: str = None
    headers: dict = None
    body: str = None

@dataclass
class HttpResponse(Message):
    status_code: int = None
    headers: dict = None
    body: str = None