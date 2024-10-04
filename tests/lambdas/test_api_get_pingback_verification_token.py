from unittest import mock

import respx

from src.lambdas import api_get_pingback_verification_token
from src.layers.testing import CSTestFixture
from src.layers.twocaptcha import api_twocaptcha


class ApiGetPingbackVerificationTokenTests(CSTestFixture):
    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_pingback_token')
    def test_ok(
        self,
        mocked_get_pingback_token
    ):
        mocked_get_pingback_token.return_value = self.TEST_VERIFICATION_TOKEN

        mock_event = self.get_event_resource_json('event#api_get_pingback_verification_token.json')

        val = api_get_pingback_verification_token.lambda_handler(event=mock_event, context=None)
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
