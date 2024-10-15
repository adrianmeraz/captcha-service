from unittest import mock

from src.lambdas import api_post_report_bad_captcha
from src.layers.captcha_service import CaptchaService
from src.layers.testing import CSTestFixture


class ApiPostReportBadCaptchaTests(CSTestFixture):

    @mock.patch.object(CaptchaService, 'report_bad_captcha_id')
    def test_ok(
        self,
        mocked_report_bad_captcha_id
    ):
        mocked_report_bad_captcha_id.return_value = True

        mock_event = self.get_event_resource_json('event#api_post_report_bad_captcha.json')

        val = api_post_report_bad_captcha.lambda_handler(event=mock_event, context=None)
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
