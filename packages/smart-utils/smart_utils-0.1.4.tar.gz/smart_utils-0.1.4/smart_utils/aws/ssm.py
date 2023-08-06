import logging
from . import AWSClient

SSM_SERVICE = 'ssm'

class AWSClientSSM(AWSClient):

    def __init__(self, access_key=None, secret_key=None):
        super().__init__(SSM_SERVICE, access_key, secret_key)


    def get_parameter(self, name):

        try:
            parameter = self.client.get_parameter(
                Name=name,
                WithDecryption=True
            )
            return parameter["Parameter"]["Value"]

        except Exception as e:
            logging.warning(f"Parameter {name} not Found in SSM - {e}")
            
