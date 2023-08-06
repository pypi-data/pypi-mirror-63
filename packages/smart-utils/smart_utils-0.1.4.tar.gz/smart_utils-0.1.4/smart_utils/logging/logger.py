import logging.config
import yaml
from yaml.scanner import ScannerError
from yaml.parser import ParserError

from importlib import import_module
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from smart_utils.logging.config import ConfigGetter

DEFAULT_FORMAT = '%(asctime)s - [%(levelname)s] - %(module)s - %(funcName)s  - %(message)s'
logging.basicConfig(format=DEFAULT_FORMAT, level=logging.INFO)


class LoggerConstructor:

    def __init__(self, getter:ConfigGetter, environment):

        self.getter = getter
        self.environment = environment


    def __load_configuration(self,yml_config):

        try:
            logging_config = yaml.safe_load(yml_config)
            logging.config.dictConfig(logging_config)
            logging.info("Loaded setting of .yml")
            return "main"
        except (ValueError, ScannerError,ParserError):
            logging.error("Configuration failed to load, review yml. Getting generic logger")


    def __import_class(self, name):
        components = name.split('.')
        module = import_module(".".join(components[:-1]))
        _class = getattr(module, components[-1])
        return _class

    def __get_integrations(self, integrations):
        result = [
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
        ]

        for integration, args in integrations.items():
            try:
                module = self.__import_class(integration)
                result.append(module(**args))
            except Exception as ex:
                logging.error(f'Fail to append integration {integration} - {ex}')

        return result

    def _activate_sentry(self, sentry_dsn, integrations):

        try:
            sentry_sdk.init(
                environment = self.environment,
                dsn=sentry_dsn,
                integrations=self.__get_integrations(integrations),
            )
            return True
        except Exception as e:
            logging.error("Error to activate Sentry {}".format(e))
            return False


    def generate_logger(self):

        yml_config, sentry_dsn, sentry_integrations = self.getter.get_config()
        logging_name = None
        if yml_config:
            logging_name = self.__load_configuration(yml_config)
            if sentry_dsn and logging_name:
                if self._activate_sentry(sentry_dsn, sentry_integrations):
                    logging.info("Activate Sentry")
        return logging.getLogger(logging_name)



