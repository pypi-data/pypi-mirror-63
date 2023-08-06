import json
import logging
from os import getenv
from abc import ABCMeta, abstractmethod
from smart_utils.aws.ssm import AWSClientSSM


ACCESS_KEY = getenv('AWS_ACCESS_KEY_ID', None)
SECRET_KEY = getenv('AWS_SECRET_ACCESS_KEY', None)


class ConfigGetter:

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_config(self):
        pass


class ConfigGetterAws(ConfigGetter):

    def __init__(self, app_name):

        self.client = AWSClientSSM(ACCESS_KEY, SECRET_KEY)
        self.app_name = getenv("LOGGING_CONFIG", app_name)
        self.sentry_dsn_name = getenv("SENTRY_DSN", f"SENTRY_DSN_{app_name}")
        self.sentry_integrations = "SENTRY_INTEGRATIONS"

    def get_config(self):
        yml_config = None
        sentry_dsn = None
        sentry_integrations = None

        try:
            yml_config = self.client.get_parameter(self.app_name)
            sentry_dsn = self.client.get_parameter(self.sentry_dsn_name)
            sentry_integrations = json.loads(self.client.get_parameter(self.sentry_integrations))

            if not yml_config and not self.app_name == "default":
                yml_config = self.client.get_parameter("default")
                sentry_dsn = None
                logging.warning(f"Configuration {self.app_name} not found, default was obtained")
        except Exception as e:
            logging.warning(f"Error in the SSM-AWS process: {e}, configuration-generic was obtained")

        finally:
            return yml_config, sentry_dsn, sentry_integrations
