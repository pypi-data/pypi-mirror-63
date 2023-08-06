import json
import unittest
from unittest.mock import patch
from smart_utils.logging.config import ConfigGetter, ConfigGetterAws
from smart_utils.aws.ssm import AWSClientSSM

from abc import ABCMeta


class TestConfigGetter(unittest.TestCase):

    def setUp(self):
        self.test_instance = ConfigGetter()

    def test_init(self):
        self.assertTrue(isinstance(self.test_instance, ConfigGetter))
        self.assertEqual(self.test_instance.__metaclass__, ABCMeta)

    def test_get_config(self):
        self.assertEqual(self.test_instance.get_config(), None)


class TestConfigGetterAWS(unittest.TestCase):

    @patch('smart_utils.logging.config.AWSClientSSM')
    def setUp(self, mock_aws_client):
        self.mock_aws_client = mock_aws_client
        self.test_app = 'Test App'
        self.test_instance = ConfigGetterAws(self.test_app)

    def test_init(self):

        self.assertEqual(self.test_instance.app_name, self.test_app)
        self.assertEqual(self.test_instance.sentry_dsn_name, f"SENTRY_DSN_{self.test_app}")
        self.assertEqual(self.test_instance.client, self.mock_aws_client.return_value)

    def test_get_config(self):
        test_yml_value = 'yml-value'
        test_dsn_value = 'dsn-value'
        test_integrations_value = {}
        test_default_value = 'default-value'

        self.mock_aws_client.return_value.get_parameter.side_effect = [x for x in [test_yml_value, test_dsn_value, json.dumps(test_integrations_value), test_default_value]]
        self.assertEqual(self.test_instance.get_config(), (test_yml_value, test_dsn_value, test_integrations_value))
        self.assertEqual(self.mock_aws_client.return_value.get_parameter.call_count, 3)

    def test_get_config_default(self):
        test_yml_value = None
        test_dsn_value = None
        test_integrations_value = "{}"
        test_default_value = 'default-value'

        self.mock_aws_client.return_value.get_parameter.side_effect = [x for x in [test_yml_value, test_dsn_value, json.dumps(test_integrations_value), test_default_value]]
        self.assertEqual(self.test_instance.get_config(), (test_default_value, None, test_integrations_value))
        self.assertEqual(self.mock_aws_client.return_value.get_parameter.call_count, 4)

    def test_get_config_raise(self):
        self.mock_aws_client.return_value.get_parameter.side_effect = Exception('test error')
        self.assertEqual(self.test_instance.get_config(), (None, None, None))
        self.assertEqual(self.mock_aws_client.return_value.get_parameter.call_count, 1)
        
