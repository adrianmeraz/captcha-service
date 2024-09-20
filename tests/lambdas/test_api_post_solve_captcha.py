from unittest import mock

import respx
from py_aws_core.db_dynamo import DDBClient

from src.lambdas import api_post_solve_captcha
from src.layers.testing import CSTestFixture
from src.layers.twocaptcha import api_twocaptcha


class ApiPostSolveCaptchaTests(CSTestFixture):
    @respx.mock
    @mock.patch.object(DDBClient, 'batch_write_item_maps')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_environment')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_app_name')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_base_domain_name')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_ok(
        self,
        mocked_get_api_key,
        mocked_get_domain_name,
        mocked_get_app_name,
        mocked_get_environment,
        mocked_batch_write_item_maps
    ):
        mocked_get_api_key.return_value = 'IPSUMKEY'
        mocked_get_domain_name.return_value = 'ipsumlorem.com'
        mocked_get_app_name.return_value = 'big-service'
        mocked_get_environment.return_value = 'dev'

        mocked_batch_write_item_maps.return_value = 1

        mocked_solve_captcha = self.create_ok_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fwww.example.com&json=1&proxy=&proxytype=MEGAPROXY.ROTATING.PROXYRACK.NET&pingback=https%3A%2F%2Fbig-service-dev.ipsumlorem.com%2Fpingback-event',
            _json=self.get_api_resource_json('get_captcha_id.json')
        )

        mock_event = self.get_event_resource_json('event#api_post_solve_captcha.json')

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
        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_get_domain_name.call_count, 1)
        self.assertEqual(mocked_get_app_name.call_count, 1)
        self.assertEqual(mocked_get_environment.call_count, 1)

        self.assertEqual(mocked_batch_write_item_maps.call_count, 1)
