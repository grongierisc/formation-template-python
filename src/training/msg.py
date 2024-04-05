from grongier.pex import Message
from dataclasses import dataclass

@dataclass
class Training:
    id: str = None
    name: str = None
    room: str = None

@dataclass
class TrainingMessage(Message):
    training: Training
    to_orm: bool = False
    verbe: str = 'POST'
    training_list: list = None

@dataclass
class TrainingOrmMessage(Message):
    training: Training

@dataclass
class TrainingAck(Message):
    to_db: bool = False