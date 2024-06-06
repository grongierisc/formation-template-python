from grongier.pex import BusinessOperation

import requests

from iris_fhir.msg import FhirRequest, FhirResponse

class FhirHttpOperation(BusinessOperation):

    def on_init(self):
        if not hasattr(self, 'url'):
            self.url = 'http://host.docker.internal:33783/fhir/r4'
        if not hasattr(self, 'credential'):
            self.credential = 'SuperUser'

        self.session = requests.Session()
        self.session.auth = self._get_credentials()

    def _get_credentials(self) -> tuple:
        if self.credential == 'SuperUser':
            return ('SuperUser', 'SYS')
        else:
            return ('', '')
        
    def on_fhir_request(self, msg: FhirRequest):
        uri = msg.url or self.url
        uri = uri.rstrip('/') + '/' + msg.resource
        response = self.session.request(
            method=msg.method,
            url=uri,
            data=msg.data,
            headers=msg.headers,
            timeout=10,
            verify=False
        )
        return FhirResponse(
            status_code=response.status_code,
            content=response.text,
            headers=response.headers,
            resource=msg.resource
        )