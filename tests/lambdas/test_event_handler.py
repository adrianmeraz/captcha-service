from unittest import mock

import respx
from py_aws_core.db_dynamo import DDBClient

from src.lambdas import event_handler
from src.layers.testing import CSTestFixture
from src.layers.twocaptcha.captcha import TwoCaptcha


class EventHandlerTests(CSTestFixture):
    @respx.mock
    @mock.patch.object(TwoCaptcha, 'solve_captcha')
    def test_solve_captcha_ok(
        self,
        mocked_solve_captcha,
    ):
        mocked_solve_captcha.return_value = True

        mock_event = self.get_event_resource_json('event#api_post_solve_captcha.json')

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

    @mock.patch.object(TwoCaptcha, 'send_webhook_event')
    @mock.patch.object(DDBClient, 'put_item')
    @mock.patch.object(DDBClient, 'update_item')
    def test_solve_captcha_ok(
        self,
        mocked_update_item,
        mocked_put_item,
        mocked_send_webhook_event,
    ):
        mock_event = self.get_event_resource_json('event#api_post_pingback_event.json')

        mocked_update_item.return_value = self.get_db_resource_json('db#update_captcha_event.json')
        mocked_send_webhook_event.return_value = True
        mocked_put_item.return_value = dict()

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

        self.assertEqual(mocked_update_item.call_count, 1)
        self.assertEqual(mocked_send_webhook_event.call_count, 1)
