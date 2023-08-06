import unittest
from unittest.mock import patch
from smart_utils.aws import AWSClient


class TestAWSClient(unittest.TestCase):

    def setUp(self):
        self.test_service = 'test_service'
        self.access_key = 'test_access_key'
        self.secret_key = 'test_secret_key'

    @patch('smart_utils.aws.AWSClient._AWSClient__get_client')
    def test__init(self, mock_get_client):

        test_instance = AWSClient(self.test_service, self.access_key, self.secret_key)

        self.assertEqual(test_instance.service, self.test_service)
        self.assertEqual(test_instance.access_key, self.access_key)
        self.assertEqual(test_instance.secret_key, self.secret_key)
        self.assertEqual(mock_get_client.call_count, 1)
        self.assertEqual(test_instance.client, mock_get_client.return_value)

    @patch('smart_utils.aws.AWSClient._AWSClient__get_client')
    def test__has_aws_credentials(self, mock_get_client):
        test_instance = AWSClient(self.test_service, self.access_key, self.secret_key)
        self.assertTrue(test_instance._AWSClient__has_aws_credentials())

    @patch('smart_utils.aws.AWSClient._AWSClient__get_client')
    def test__not_has_aws_credentials(self, mock_get_client):

        test_instance = AWSClient(self.test_service, self.access_key, None)
        self.assertFalse(test_instance._AWSClient__has_aws_credentials())

        test_instance = AWSClient(self.test_service, None, self.secret_key)
        self.assertFalse(test_instance._AWSClient__has_aws_credentials())

        test_instance = AWSClient(self.test_service, None, None)
        self.assertFalse(test_instance._AWSClient__has_aws_credentials())

    @patch('smart_utils.aws.AWSClient._AWSClient__get_client_with_params')
    @patch('smart_utils.aws.AWSClient._AWSClient__get_client_with_config')
    def test__get_client_with_creedentials(self, mock_getClientConfig, mock_getClientParams):

        self.assertEqual(mock_getClientConfig.call_count, 0)
        self.assertEqual(mock_getClientConfig.call_count, 0)

        test_instance = AWSClient(self.test_service, self.access_key, self.secret_key)
        self.assertEqual(mock_getClientParams.call_count, 1)
        self.assertEqual(mock_getClientConfig.call_count, 0)
        self.assertEqual(test_instance.client, mock_getClientParams.return_value)

    @patch('smart_utils.aws.AWSClient._AWSClient__get_client_with_params')
    @patch('smart_utils.aws.AWSClient._AWSClient__get_client_with_config')
    def test__get_client_without_creedentials(self, mock_getClientConfig, mock_getClientParams):

        self.assertEqual(mock_getClientConfig.call_count, 0)
        self.assertEqual(mock_getClientConfig.call_count, 0)

        test_instance = AWSClient(self.test_service, self.access_key, None)
        self.assertEqual(mock_getClientParams.call_count, 0)
        self.assertEqual(mock_getClientConfig.call_count, 1)
        self.assertEqual(test_instance.client, mock_getClientConfig.return_value)

    @patch('smart_utils.aws.AWSClient._AWSClient__has_aws_credentials')
    def test__get_client_raise(self, mock_has_credentials):
        mock_has_credentials.side_effect = Exception('Test exception')

        test_instance = AWSClient(self.test_service, self.access_key, None)
        self.assertEqual(test_instance.client, None)
