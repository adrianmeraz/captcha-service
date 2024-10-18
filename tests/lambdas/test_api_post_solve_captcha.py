from unittest import mock

import respx
from py_aws_core.boto_clients import DynamoDBClientFactory

from src.lambdas import api_post_solve_captcha
from src.layers.captcha_service import CaptchaService
from src.layers.db_service import DatabaseService
from src.layers.secrets import Secrets
from src.layers.testing import CSTestFixture


class ApiPostSolveCaptchaTests(CSTestFixture):
    @respx.mock
    @mock.patch.object(CaptchaService, 'solve_captcha')
    def test_ok(
        self,
        mocked_solve_captcha,
    ):
        mocked_solve_captcha.return_value = True

        mock_event = self.get_event_resource_json('event#api_post_solve_captcha.json')

        boto_client = DynamoDBClientFactory.new_client()
        secrets = Secrets(_dynamo_db_table_name='TEST_TABLE', _twocaptcha_pingback_token=self.TEST_VERIFICATION_TOKEN)
        db_service = DatabaseService(boto_client=boto_client, secrets=secrets)
        captcha_service = CaptchaService(db_service=db_service, secrets=secrets)
        val = api_post_solve_captcha.lambda_handler(event=mock_event, context=None, captcha_service=captcha_service)
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
