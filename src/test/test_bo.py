from bo import IrisTrainingOperation
from msg import Training

from unittest.mock import MagicMock
import iris

class TestBo():
    def test_get_training_with_empty_id(self):
        bo = IrisTrainingOperation()
        # Mock the call to iris.sql.exec and return an empty list
        iris.sql.exec = MagicMock(return_value=[])

        training = bo.get_training(Training(id=''))
        assert training.training_list is not None
        assert len(training.training_list) == 0
        
        

    def test_get_training_with_existing_id(self):
        # TODO: Write test case for get_training method when training id exists
        pass

    def test_get_all_training(self):
        bo = IrisTrainingOperation()
        training = bo.get_training(Training(id=''))
        assert training.training_list is not None
