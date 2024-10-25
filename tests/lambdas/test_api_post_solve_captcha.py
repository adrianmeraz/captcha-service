from unittest import mock

import respx
from botocore.stub import Stubber
from py_aws_core.boto_clients import DynamoDBClientFactory, DynamoTableFactory

from src.lambdas import api_post_solve_captcha
from src.layers.captcha_service import CaptchaService
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

        table = DynamoTableFactory.new_client(table_name='TEST_TABLE')
        stubber = Stubber(table.meta.client)
        stubber.activate()

        captcha_service = self.get_mock_captcha_service(table=table)
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

        stubber.assert_no_pending_responses()
