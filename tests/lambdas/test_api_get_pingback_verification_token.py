import respx
from py_aws_core.boto_clients import DynamoDBClientFactory

from src.lambdas import api_get_pingback_verification_token
from src.layers.captcha_service import CaptchaService
from src.layers.db_service import DatabaseService
from src.layers.secrets import Secrets
from src.layers.testing import CSTestFixture


class ApiGetPingbackVerificationTokenTests(CSTestFixture):
    @respx.mock
    def test_ok(self):
        mock_event = self.get_event_resource_json('event#api_get_pingback_verification_token.json')

        boto_client = DynamoDBClientFactory.new_client()
        captcha_service = self.get_mock_captcha_service(boto_client=boto_client)
        val = api_get_pingback_verification_token.lambda_handler(
            event=mock_event,
            context=None,
            captcha_service=captcha_service
        )
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
