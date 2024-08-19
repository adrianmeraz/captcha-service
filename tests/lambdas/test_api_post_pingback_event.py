import json
from importlib.resources import as_file
from unittest import mock

from py_aws_core.testing import BaseTestFixture

from src.lambdas import api_post_pingback_event
from src.layers.twocaptcha.services import TwoCaptchaService
from tests import const as test_const

RESOURCE_PATH = test_const.TEST_API_RESOURCE_PATH


class ApiPostSolveCaptchaTests(BaseTestFixture):

    @mock.patch.object(TwoCaptchaService, 'handle_webhook_event')
    def test_ok(
        self,
        mocked_handle_webhook_event
    ):
        source = test_const.TEST_EVENT_RESOURCE_PATH.joinpath('event#api_post_pingback_event.json')
        with as_file(source) as event_json:
            mock_event = json.loads(event_json.read_text())

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

        self.assertEqual(mocked_handle_webhook_event.call_count, 1)
