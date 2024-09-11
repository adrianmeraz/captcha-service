import json
from importlib.resources import as_file
from unittest import mock

from py_aws_core.db_dynamo import DDBClient
from py_aws_core.testing import BaseTestFixture

from src.lambdas import api_post_pingback_event
from src.layers.twocaptcha.captcha import TwoCaptcha
from tests import const as test_const

RESOURCE_PATH = test_const.TEST_API_RESOURCE_PATH


class ApiPostPingbackEventTests(BaseTestFixture):

    @mock.patch.object(TwoCaptcha, 'send_webhook_event')
    @mock.patch.object(DDBClient, 'put_item')
    @mock.patch.object(DDBClient, 'update_item')
    def test_ok(
        self,
        mocked_update_item,
        mocked_put_item,
        mocked_send_webhook_event
    ):
        source = test_const.TEST_EVENT_RESOURCE_PATH.joinpath('event#api_post_pingback_event.json')
        with as_file(source) as event_json:
            mock_event = json.loads(event_json.read_text())

        source = test_const.TEST_DB_RESOURCE_PATH.joinpath('db#update_captcha_event.json')
        with as_file(source) as db_update_captcha_event_json:
            mocked_update_item.return_value = json.loads(db_update_captcha_event_json.read_text())
        mocked_send_webhook_event.return_value = True
        mocked_put_item.return_value = True

        val = api_post_pingback_event.lambda_handler(raw_event=mock_event, context=None)
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
