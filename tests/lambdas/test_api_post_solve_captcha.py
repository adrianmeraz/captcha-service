import json
from importlib.resources import as_file
from unittest import mock

import respx
from py_aws_core.testing import BaseTestFixture

from src.lambdas import api_post_solve_captcha
from src.layers.twocaptcha import api_twocaptcha
from tests import const as test_const

RESOURCE_PATH = test_const.TEST_API_RESOURCE_PATH


class ApiPostSolveCaptchaTests(BaseTestFixture):
    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_ok(
        self,
        mocked_get_api_key
    ):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = RESOURCE_PATH.joinpath('get_captcha_id.json')
        with as_file(source) as get_captcha_id_json:
            mocked_solve_captcha = self.create_ok_route(
                method='POST',
                url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fwww.example.com&json=1&proxy=&proxytype=MEGAPROXY.ROTATING.PROXYRACK.NET&pingback=https%3A%2F%2Fwww.example.com%2Fcaptcha_pingback',
                _json=json.loads(get_captcha_id_json.read_text(encoding='utf-8'))
            )

        source = test_const.TEST_EVENT_RESOURCE_PATH.joinpath('event#api_post_solve_captcha.json')
        with as_file(source) as event_json:
            mock_event = json.loads(event_json.read_text())

        val = api_post_solve_captcha.lambda_handler(raw_event=mock_event, context=None)
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
