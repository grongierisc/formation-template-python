from hello_world.bo import HelloWorldBO

from training.bo import FormationFileBO

from training.bs import FormationCSVService

from training.bp import FormationBP

from training.bo import HttpBO
from iris_fhir import bp, bs, bo

CLASSES = {
    'Python.HelloWorldBO': HelloWorldBO,
    'Python.FormationFileBO': FormationFileBO,
    'Python.FormationCSVService': FormationCSVService,
    'Python.FormationBP': FormationBP,
    'Python.HttpBO': HttpBO,
    'Python.CsvToFhir': bp.CsvToFhir,
    'Python.FhirCsvService': bs.FhirCSVService,
    'Python.FhirHttpOperation': bo.FhirHttpOperation,

}
