from bo import WriteTrainingFileOperation, TrainingPostgresOperation, IrisTrainingOperation
from bs import TrainingPoolingService, TrainingRestService
from bp import TrainingProcess
from bo import ReadTrainingFromIrisOperation

CLASSES = {
    'Python.WriteTrainingFileOperation': WriteTrainingFileOperation,
    'Python.TrainingPoolingService': TrainingPoolingService,
    'Python.TrainingPostgresOperation': TrainingPostgresOperation,
    'Python.TrainingProcess': TrainingProcess,
    'Python.IrisTrainingOperation': IrisTrainingOperation,
    'Python.TrainingRestService': TrainingRestService,
    'Python.ReadTrainingFromIrisOperation': ReadTrainingFromIrisOperation
}
