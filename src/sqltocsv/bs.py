from grongier.pex import BusinessService
import pandas as pd
from sqlalchemy import create_engine


from .msg import SQLMessage

class SQLService(BusinessService):

    def __init__(self, **kwargs):
        self.sql = None
        self.conn = None
        self.target = None

    def on_init(self):
        if not hasattr(self, 'sql'):
            raise Exception('Missing sql attribute')
        if not hasattr(self, 'conn'):
            raise Exception('Missing conn attribute')
        if not hasattr(self, 'target'):
            raise Exception('Missing target attribute')
        
        self.engine = create_engine(self.conn)

        # raise an error if cannot connect to the database
        self.engine.connect()

    def get_adapter_type():
        """
        Name of the registred Adapter
        """
        return "Ens.InboundAdapter"
    
    def on_process_input(self, message_input):
        # create a dataframe from the sql query
        df = pd.read_sql(self.sql, self.engine)
        # create a message
        message = SQLMessage(dataframe=df)
        # send the message to the target
        self.send_request_sync(self.target, message)
        return