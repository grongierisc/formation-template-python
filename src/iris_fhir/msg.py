from grongier.pex import Message
from dataclasses import dataclass

# create a dataclass for this csv :
# id;name;surname;address;phone;city;zipcode;country;email;genre;birthdate
@dataclass
class Patient:
    id: str
    name: str
    surname: str
    address: str
    phone: str
    city: str
    zipcode: str
    country: str
    email: str
    genre: str
    birthdate: str

@dataclass
class PatientRequest(Message):
    patient: Patient

@dataclass
class FhirRequest(Message):
    url: str
    resource: str
    method: str
    data: str
    headers: dict

@dataclass
class FhirResponse(Message):
    status_code: int
    content: str
    headers: dict
    resource: str