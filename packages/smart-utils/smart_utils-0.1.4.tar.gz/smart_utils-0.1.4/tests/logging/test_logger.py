import pytest
from smart_utils.logging import LoggerConstructor
from smart_utils.logging.config import ConfigGetter


class ConfigGetterTest(ConfigGetter):

    def __init__(self,yml,sentry_dsn, integrations):
        self.yml = yml
        self.sentry_dsn = sentry_dsn
        self.integrations = integrations

    def get_config(self):
        return self.yml, self.sentry_dsn, self.integrations


def test_init(yml,sentry_dsn,integrations):

    Logger = LoggerConstructor(ConfigGetterTest(yml,sentry_dsn,integrations),"test")
    assert Logger.environment == "test"
    assert isinstance(Logger.getter,ConfigGetter)

def test_activate_sentry_error(yml,sentry_dsn,integrations):

    Logger = LoggerConstructor(ConfigGetterTest(yml,sentry_dsn,integrations),"test")
    assert Logger._activate_sentry(sentry_dsn, integrations) == False

def test_generate_logger_loaded(yml,sentry_dsn,integrations):

    Logger = LoggerConstructor(ConfigGetterTest(yml,sentry_dsn,integrations),"test")
    assert Logger.generate_logger().name == 'main'

def test_generate_logger_error(yml_error,sentry_dsn,integrations):

    Logger = LoggerConstructor(ConfigGetterTest(yml_error,sentry_dsn,integrations),"test")
    assert Logger.generate_logger().name == 'root'

def test_generate_logger_yml_none(yml_none,sentry_dsn,integrations):

    Logger = LoggerConstructor(ConfigGetterTest(yml_none,sentry_dsn,integrations),"test")
    assert Logger.generate_logger().name == 'root'

def test_integrations(yml_none,sentry_dsn,django_integrations):

    Logger = LoggerConstructor(ConfigGetterTest(yml_none,sentry_dsn,django_integrations),"test")
    integrations_formated = Logger._LoggerConstructor__get_integrations(django_integrations)

    installed_integration_modules = 0

    for integration in django_integrations.keys():
        try:
            Logger._LoggerConstructor__import_class(integration)
            installed_integration_modules += 1
        except Exception as ex:
            continue

    assert len(integrations_formated) == installed_integration_modules + 1
