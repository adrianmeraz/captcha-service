from unittest import mock

import respx
from py_aws_core.boto_clients import SSMClientFactory
from py_aws_core.clients import RetryClient

from src.layers.captcha_service import CaptchaService
from src.layers.db_service import DatabaseService
from src.layers.testing import CSTestFixture
from src.layers.twocaptcha import api_twocaptcha, tc_db_dynamo


class CaptchaServiceTests(CSTestFixture):
    """
        Get Captcha ID Tests
    """

    @respx.mock
    @mock.patch.object(DatabaseService, 'update_captcha_event_on_solve_attempt')
    @mock.patch.object(DatabaseService, 'get_or_create_recaptcha_v2_event')
    def test_solve_captcha_ok(
        self,
        mocked_get_or_create_recaptcha_v2_event,
        mocked_update_captcha_event_on_solve_attempt,
    ):
        mocked_get_or_create_recaptcha_v2_event.return_value = 1
        mocked_update_captcha_event_on_solve_attempt.return_value = 1
        mocked_solve_captcha = self.create_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=test-password-1&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&pingback=https%3A%2F%2Fbig-service-dev.ipsumlorem.com%2Fpingback-event',
            response_status_code=200,
            response_json=self.get_api_resource_json('get_captcha_id.json')
        )

        with RetryClient() as client:
            boto_client = SSMClientFactory.new_client()
            captcha_service = self.get_mock_captcha_service(boto_client=boto_client)
            captcha_service.solve_captcha(
                http_client=client,
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com',
                webhook_url='https://ipsumlorem.com/webhook'
            )

        self.assertEqual(mocked_get_or_create_recaptcha_v2_event.call_count, 1)
        self.assertEqual(mocked_update_captcha_event_on_solve_attempt.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @mock.patch.object(tc_db_dynamo.CreateTCWebhookEvent, 'call')
    @mock.patch.object(DatabaseService, 'update_captcha_event_code')
    def test_handle_webhook_event_ok(
        self,
        mocked_update_captcha_event_code,
        mocked_create_tc_webhook_event_call
    ):
        mocked_report_bad_captcha = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportbad&id=2122988149&json=1',
            response_status_code=200,
            response_json=self.get_api_resource_json('invalid_response.json')
        )
        mocked_update_captcha_event_code.return_value = True
        mocked_create_tc_webhook_event_call.return_value = True

        boto_client = SSMClientFactory.new_client()
        captcha_service = self.get_mock_captcha_service(boto_client=boto_client)

        with RetryClient() as client:
            captcha_service.handle_webhook_event(
                http_client=client,
                captcha_id='9991117777',
                code=self.TEST_RECAPTCHA_V2_TOKEN,
                rate='.00299'
            )

        self.assertEqual(mocked_update_captcha_event_code.call_count, 1)
        self.assertEqual(mocked_create_tc_webhook_event_call.call_count, 1)

    @respx.mock
    @mock.patch.object(DatabaseService, 'update_captcha_event_webhook')
    def test_send_webhook_event_ok(
        self,
        mocked_update_captcha_event_webhook
    ):
        mocked_update_captcha_event_webhook.return_value = True

        mocked_post_webhook = self.create_route(
            method='POST',
            url__eq='http://mysite.com/pingback/url/',
            response_status_code=200,
            response_text=''
        )

        boto_client = SSMClientFactory.new_client()
        captcha_service = self.get_mock_captcha_service(boto_client=boto_client)

        with RetryClient() as client:
            webhook_data = {
                'test1': 'val1',
                'test33': 'ipsum lorem'
            }
            captcha_service.send_webhook_event(
                http_client=client,
                captcha_id='9991117777',
                captcha_token=self.TEST_RECAPTCHA_V2_TOKEN,
                webhook_url='http://mysite.com/pingback/url/',
                webhook_data=webhook_data,
            )

        self.assertEqual(mocked_post_webhook.call_count, 1)
        self.assertEqual(mocked_update_captcha_event_webhook.call_count, 1)

    @respx.mock
    def test_get_verification_token_ok(self):
        boto_client = SSMClientFactory.new_client()
        captcha_service = self.get_mock_captcha_service(boto_client=boto_client)
        r = captcha_service.get_verification_token()

        self.assertEqual(r, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c')

    @mock.patch.object(tc_db_dynamo.CreateTCCaptchaReport, 'call')
    @mock.patch.object(api_twocaptcha.ReportBadCaptcha, 'call')
    def test_report_bad_captcha_id_ok(
        self,
        mocked_report_bad_captcha,
        mocked_create_tc_captcha_report
    ):
        mocked_report_bad_captcha.return_value = True
        mocked_create_tc_captcha_report.return_value = True

        with RetryClient() as client:
            boto_client = SSMClientFactory.new_client()
            captcha_service = self.get_mock_captcha_service(boto_client=boto_client)
            captcha_service.report_bad_captcha_id(
                http_client=client,
                captcha_id='9991117777'
            )

        self.assertEqual(mocked_report_bad_captcha.call_count, 1)
        self.assertEqual(mocked_create_tc_captcha_report.call_count, 1)

    @mock.patch.object(tc_db_dynamo.CreateTCCaptchaReport, 'call')
    @mock.patch.object(api_twocaptcha.ReportGoodCaptcha, 'call')
    def test_report_good_captcha_id_ok(
        self,
        mocked_report_good_captcha,
        mocked_create_tc_captcha_report
    ):
        mocked_report_good_captcha.return_value = True
        mocked_create_tc_captcha_report.return_value = True

        with RetryClient() as client:
            boto_client = SSMClientFactory.new_client()
            captcha_service = self.get_mock_captcha_service(boto_client=boto_client)
            captcha_service.report_good_captcha_id(
                http_client=client,
                captcha_id='9991117777'
            )

        self.assertEqual(mocked_report_good_captcha.call_count, 1)
        self.assertEqual(mocked_create_tc_captcha_report.call_count, 1)
