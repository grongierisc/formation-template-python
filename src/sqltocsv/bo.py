from grongier.pex import BusinessOperation
from .msg import SQLMessage

import pandas as pd

class CSVOperation(BusinessOperation):

    def __init__(self, **kwargs):
        self.filename = None

    def on_init(self):
        if not hasattr(self, 'filename'):
            raise Exception('Missing filename attribute')
        
    def on_sql_message(self, message_input: SQLMessage):
        # get the dataframe from the message
        df = message_input.dataframe
        # create a csv file
        df.to_csv(self.filename, index=False)
        return