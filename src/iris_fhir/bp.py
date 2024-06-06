from grongier.pex import BusinessProcess
from iris_fhir.msg import PatientRequest, FhirRequest

from fhir.resources.R4B.patient import Patient as FhirPatient
from fhir.resources.R4B.humanname import HumanName
from fhir.resources.R4B.contactpoint import ContactPoint
from fhir.resources.R4B.address import Address
from fhir.resources.R4B.identifier import Identifier
from fhir.resources.R4B.bundle import Bundle


class CsvToFhir(BusinessProcess):

    def on_csv_to_fhir(self, request: PatientRequest):
        # create a FHIR Patient resource
        fhir_patient = FhirPatient(active=True)
        # map the data from the csv to the FHIR Patient resource
        # csv : id;name;surname;address;phone;city;zipcode;country;email;genre;birthdate
        # create a HumanName resource
        human_name = HumanName()
        human_name.family = request.patient.name
        human_name.given = [request.patient.surname]
        fhir_patient.name = [human_name]
        # create a ContactPoint resource
        contact_point = ContactPoint()
        contact_point.system = "phone"
        contact_point.value = request.patient.phone
        fhir_patient.telecom = [contact_point]
        # add the email too
        contact_point = ContactPoint()
        contact_point.system = "email"
        contact_point.value = request.patient.email
        fhir_patient.telecom.append(contact_point)
        # create an Address resource
        address = Address()
        address.line = [request.patient.address]
        address.city = request.patient.city
        address.postalCode = request.patient.zipcode
        address.country = request.patient.country
        fhir_patient.address = [address]
        # create an Identifier resource
        identifier = Identifier()
        identifier.system = "http://icp.org/patient"
        identifier.value = request.patient.id
        fhir_patient.identifier = [identifier]
        # and the birthdate please
        fhir_patient.birthDate = request.patient.birthdate

        # create bundle with conditional update
        bundle = self.create_bundle(fhir_patient)

        # create the FhirRequest message
        fhir_request = FhirRequest(
            url=None,
            resource='/',
            method='POST',
            data=bundle.json(),
            headers={'Accept': 'application/json',
                     'Content-Type': 'application/json+fhir'}
        )

        # send the FhirRequest message to the next Business Operation
        self.send_request_sync("Python.FhirHttpOperation", fhir_request)

    def create_bundle(self, fhir_patient: FhirPatient) -> Bundle:
        bundle = Bundle(type="transaction")
        bundle.entry = [
            {"resource": fhir_patient, "request":
             {"method": "PUT",
              "url": "Patient?identifier=http://icp.org/patient|"+fhir_patient.identifier[0].value,
              "ifNoneExist": "Patient?identifier=http://icp.org/patient|"+fhir_patient.identifier[0].value
              }
             }
        ]
        return bundle
