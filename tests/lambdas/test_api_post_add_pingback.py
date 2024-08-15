import json
from importlib.resources import as_file
from unittest import mock

import respx
from py_aws_core.testing import BaseTestFixture

from src.lambdas import api_post_add_pingback
from src.layers.twocaptcha import api_twocaptcha
from tests import const as test_const

RESOURCE_PATH = test_const.TEST_API_RESOURCE_PATH


class ApiPostAddPingbackTests(BaseTestFixture):
    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_ok(
        self,
        mocked_get_api_key
    ):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = test_const.TEST_API_RESOURCE_PATH.joinpath('add_pingback.json')
        with as_file(source) as warn_error_status_json:
            mocked_add_pingback = self.create_route(
                method='GET',
                url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=add_pingback&addr=https%3A%2F%2Fniw7lgbxdd.execute-api.us-west-2.amazonaws.com%2Fdev%2Fpost-pingback-event&json=1',
                response_status_code=200,
                response_json=json.loads(warn_error_status_json.read_text(encoding='utf-8'))
            )

        source = test_const.TEST_EVENT_RESOURCE_PATH.joinpath('event#api_post_add_pingback.json')
        with as_file(source) as event_json:
            mock_event = json.loads(event_json.read_text())

        val = api_post_add_pingback.lambda_handler(raw_event=mock_event, context=None)
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

        self.assertEqual(mocked_add_pingback.call_count, 1)
