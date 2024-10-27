from unittest import mock

from botocore.stub import Stubber
from py_aws_core.boto_clients import DynamoTableFactory

from src.lambdas import api_post_report_good_captcha
from src.layers.captcha_service import CaptchaService
from src.layers.testing import CSTestFixture


class ApiPostReportGoodCaptchaTests(CSTestFixture):

    @mock.patch.object(CaptchaService, 'report_good_captcha_id')
    def test_ok(
        self,
        mocked_report_good_captcha_id
    ):
        mocked_report_good_captcha_id.return_value = True

        mock_event = self.get_event_resource_json('event#api_post_report_good_captcha.json')

        ddb_secrets = self.MockDynamoDBSecretsService()
        table = DynamoTableFactory(ddb_secrets=ddb_secrets).new_client()
        stubber = Stubber(table.meta.client)
        stubber.activate()

        captcha_service = self.get_mock_captcha_service(table=table)
        val = api_post_report_good_captcha.lambda_handler(event=mock_event, context=None, captcha_service=captcha_service)
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

        self.assertEqual(mocked_report_good_captcha_id.call_count, 1)
        stubber.assert_no_pending_responses()
