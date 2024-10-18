from unittest import mock

import respx

from botocore.stub import Stubber
from py_aws_core.boto_clients import DynamoDBClientFactory

from src.lambdas import event_handler
from src.layers.testing import CSTestFixture
from src.layers.captcha_service import CaptchaService


class EventHandlerTests(CSTestFixture):
    @respx.mock
    @mock.patch.object(CaptchaService, 'handle_webhook_event')
    @mock.patch.object(CaptchaService, 'solve_captcha')
    def test_solve_captcha_ok(
        self,
        mocked_solve_captcha,
        mocked_handle_webhook_event
    ):
        mock_event = self.get_event_resource_json('event#api_post_solve_captcha.json')
        update_json = self.get_db_resource_json('db#update_captcha_event.json')
        mocked_solve_captcha.return_value = True
        mocked_handle_webhook_event.return_value = update_json

        val = event_handler.lambda_handler(event=mock_event, context=None)
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

        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @mock.patch.object(CaptchaService, 'send_webhook_event')
    def test_solve_captcha_ok(
        self,
        mocked_send_webhook_event,
    ):
        mock_event = self.get_event_resource_json('event#api_post_pingback_event.json')
        update_json = self.get_db_resource_json('db#update_captcha_event.json')

        mocked_send_webhook_event.return_value = True

        val = event_handler.lambda_handler(event=mock_event, context=None)
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

        self.assertEqual(mocked_send_webhook_event.call_count, 1)
