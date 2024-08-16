import json
from importlib.resources import as_file
from unittest import mock

import respx
from py_aws_core.testing import BaseTestFixture

from src.lambdas import api_post_pingback_verification_token
from src.layers.twocaptcha import api_twocaptcha
from tests import const as test_const

RESOURCE_PATH = test_const.TEST_API_RESOURCE_PATH


class ApiGetPingbackVerificationTokenTests(BaseTestFixture):
    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_pingback_token')
    def test_ok(
        self,
        mocked_get_pingback_token
    ):
        mocked_get_pingback_token.return_value = test_const.TEST_VERIFICATION_TOKEN

        source = test_const.TEST_EVENT_RESOURCE_PATH.joinpath('event#api_get_pingback_verification_token.json')
        with as_file(source) as event_json:
            mock_event = json.loads(event_json.read_text())

        val = api_post_pingback_verification_token.lambda_handler(raw_event=mock_event, context=None)
        self.maxDiff = None
        self.assertEqual(
            val,
            {
                'body': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
                'multiValueHeaders': {
                    'Access-Control-Allow-Credentials': [True],
                    'Access-Control-Allow-Headers': ['Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'],
                    'Access-Control-Allow-Methods': ['DELETE,GET,POST,PUT'],
                    'Access-Control-Allow-Origin': ['*'],
                    'Content-Type': ['text/plain;charset=utf-8'],
                },
                'isBase64Encoded': False,
                'statusCode': 200
            }
        )

        self.assertEqual(mocked_get_pingback_token.call_count, 1)
