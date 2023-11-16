from grongier.pex import Message
from dataclasses import dataclass
from pandas.core.frame import DataFrame

@dataclass
class SQLMessage(Message):
    dataframe: DataFrame = None