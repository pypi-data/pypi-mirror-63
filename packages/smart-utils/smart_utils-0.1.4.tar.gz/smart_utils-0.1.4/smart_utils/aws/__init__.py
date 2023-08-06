import boto3
from botocore.exceptions import (
    ClientError,
    NoRegionError
)
import logging


class AWSClient:

    def __init__(self, service, access_key=None, secret_key=None):

        self.service = service
        self.access_key = access_key
        self.secret_key = secret_key
        self.client = self.__get_client()

    def __has_aws_credentials(self):
        return bool(self.access_key) and bool(self.secret_key)

    def __get_client(self):
        client = None

        try:
            if self.__has_aws_credentials():
                client = self.__get_client_with_params()
            else:
                client = self.__get_client_with_config()

        except Exception as e:
            logging.error("Error getting AWS client - {}".format(e))

        return client

    def __get_client_with_config(self):
        return boto3.client(self.service)

    def __get_client_with_params(self):

        return boto3.client(
                self.service,
                aws_access_key_id = self.access_key,
                aws_secret_access_key = self.secret_key,
            )
