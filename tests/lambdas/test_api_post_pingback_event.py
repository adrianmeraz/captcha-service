from unittest import mock

from src.lambdas import api_post_pingback_event
from src.layers.captcha_service import CaptchaService
from src.layers.db_dynamo import DBClient
from src.layers.testing import CSTestFixture


class ApiPostPingbackEventTests(CSTestFixture):

    @mock.patch.object(CaptchaService, 'send_webhook_event')
    @mock.patch.object(DBClient, 'put_item')
    @mock.patch.object(DBClient, 'update_item')
    def test_ok(
        self,
        mocked_update_item,
        mocked_put_item,
        mocked_send_webhook_event,
    ):
        mock_event = self.get_event_resource_json('event#api_post_pingback_event.json')

        mocked_update_item.return_value = self.get_db_resource_json('db#update_captcha_event.json')
        mocked_send_webhook_event.return_value = True
        mocked_put_item.return_value = dict()

        val = api_post_pingback_event.lambda_handler(event=mock_event, context=None)
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

        self.assertEqual(mocked_update_item.call_count, 1)
        self.assertEqual(mocked_send_webhook_event.call_count, 1)
