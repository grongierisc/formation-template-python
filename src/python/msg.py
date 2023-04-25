from dataclasses import dataclass

from grongier.pex import Message,PickleMessage

from obj import Training, Formation

from pandas import DataFrame

@dataclass
class TrainingRequest(Message):
    training:Training = None

@dataclass
class TrainingResponse(Message):
    toto:bool = False

@dataclass
class FormationRequest(Message):
    formation:Formation = None

@dataclass
class SelectTrainingRequest(Message):
    pass

@dataclass
class SelectTrainingResponse(Message):
    # list of training
    trainings:list = None

@dataclass
class SelectDataFrameRequest(Message):
    pass

@dataclass
class SelectDataFrameResponse(Message):
    # list of training
    trainings:DataFrame = None

@dataclass
class SelectDataFramePickleRequest(Message):
    pass

@dataclass
class SelectDataFramePickleResponse(PickleMessage):
    # list of training
    trainings:DataFrame = None
