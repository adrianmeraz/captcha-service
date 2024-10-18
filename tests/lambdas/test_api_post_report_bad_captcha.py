from unittest import mock

from py_aws_core.boto_clients import DynamoDBClientFactory

from src.lambdas import api_post_report_bad_captcha
from src.layers.captcha_service import CaptchaService
from src.layers.db_service import DatabaseService
from src.layers.secrets import Secrets
from src.layers.testing import CSTestFixture


class ApiPostReportBadCaptchaTests(CSTestFixture):

    @mock.patch.object(CaptchaService, 'report_bad_captcha_id')
    def test_ok(
        self,
        mocked_report_bad_captcha_id
    ):
        mocked_report_bad_captcha_id.return_value = True

        mock_event = self.get_event_resource_json('event#api_post_report_bad_captcha.json')

        boto_client = DynamoDBClientFactory.new_client()
        captcha_service = self.get_mock_captcha_service(boto_client=boto_client)
        val = api_post_report_bad_captcha.lambda_handler(event=mock_event, context=None, captcha_service=captcha_service)
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

        self.assertEqual(mocked_report_bad_captcha_id.call_count, 1)
