from unittest import mock

import respx
from botocore.stub import Stubber
from py_aws_core.boto_clients import DynamoTable
from src.layers.captcha_service import CaptchaService

from src.lambdas import event_handler
from src.layers.testing import CSTestFixture


class EventHandlerTests(CSTestFixture):
    @mock.patch.object(CaptchaService, 'solve_captcha')
    def test_routing_api_post_solve_captcha_event_ok(self, mocked_solve_captcha,):
        mocked_solve_captcha.return_value = True
        mock_event = self.get_event_resource_json('event#api_post_solve_captcha.json')

        ddb_secrets = self.MockDynamoDBSecretsService()
        dynamo_table = DynamoTable(ddb_secrets=ddb_secrets)

        captcha_service = self.get_mocked_captcha_service(dynamo_table=dynamo_table)

        val = event_handler.lambda_handler(event=mock_event, context=None, captcha_service=captcha_service)
        self.maxDiff = None
        self.assertEqual(
            val,
            {
                'body': '{}',
                'multiValueHeaders': {
                    'Access-Control-Allow-Credentials': [True],
                    'Access-Control-Allow-Headers': ['Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'],
                    'Access-Control-Allow-Methods': ['DELETE,GET,POST,PUT'],
                    'Access-Control-Allow-Origin': ['*'],
                    'Content-Type': ['application/json'],
                },
                'isBase64Encoded': False,
                'statusCode': 200
            }
        )

        self.assertEqual(1, mocked_solve_captcha.call_count)

    @respx.mock
    @mock.patch.object(CaptchaService, 'send_webhook_event')
    @mock.patch.object(CaptchaService, 'handle_webhook_event')
    def test_routing_api_post_pingback_event_ok(self, mocked_handle_webhook_event, mocked_send_webhook_event):
        mocked_handle_webhook_event.return_value = self.get_mocked_captcha_event()
        mocked_send_webhook_event.return_value = True
        mock_event = self.get_event_resource_json('event#api_post_pingback_event.json')

        ddb_secrets = self.MockDynamoDBSecretsService()
        dynamo_table = DynamoTable(ddb_secrets=ddb_secrets)

        captcha_service = self.get_mocked_captcha_service(dynamo_table=dynamo_table)
        val = event_handler.lambda_handler(event=mock_event, context=None, captcha_service=captcha_service)
        self.maxDiff = None
        self.assertEqual(
            val,
            {
                'body': '{}',
                'multiValueHeaders': {
                    'Access-Control-Allow-Credentials': [True],
                    'Access-Control-Allow-Headers': [
                        'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'],
                    'Access-Control-Allow-Methods': ['DELETE,GET,POST,PUT'],
                    'Access-Control-Allow-Origin': ['*'],
                    'Content-Type': ['application/json'],
                },
                'isBase64Encoded': False,
                'statusCode': 200
            }
        )

        self.assertEqual(1, mocked_handle_webhook_event.call_count)
        self.assertEqual(1, mocked_send_webhook_event.call_count)
