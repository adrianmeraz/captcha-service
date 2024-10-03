from unittest import mock

import respx

from src.lambdas import event_handler
from src.layers.testing import CSTestFixture
from src.layers.twocaptcha.captcha import TwoCaptcha


class EventHandlerTests(CSTestFixture):
    @respx.mock
    @mock.patch.object(TwoCaptcha, 'solve_captcha')
    def test_ok(
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
