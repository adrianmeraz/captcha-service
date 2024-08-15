import json
from importlib.resources import as_file
from unittest import mock

import respx
from py_aws_core.testing import BaseTestFixture

from src.lambdas import api_post_solve_captcha
from src.layers.twocaptcha import api_twocaptcha
from tests import const as test_const


class ApiPostSolveCaptchaTests(BaseTestFixture):
    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_ok(
        self,
        mocked_time,
    ):
        mocked_time.return_value = 1062776008  # Fri, 05 Sep 2003 15:33:28 GMT

        source = test_const.TEST_API_RESOURCE_PATH.joinpath('get_captcha_id.json')
        with as_file(source) as get_details:
            mocked_get_details = self.create_ok_route(
                method='GET',
                url__eq='https://apps.migracioncolombia.gov.co/pre-registro/es/DatosViaje',
                text=get_details.read_text(encoding='utf-8')
            )

        source = test_const.TEST_EVENT_RESOURCES_PATH.joinpath('event#travel_get_tokens.json')
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

        self.assertEqual(mocked_time.call_count, 6)
        self.assertEqual(mocked_get_details.call_count, 1)

    def test_non_cached_countries(self):
        # TODO Add the respx mock create_ok_route to all lambda tests
        pass
