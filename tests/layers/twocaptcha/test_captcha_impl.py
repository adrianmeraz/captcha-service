from unittest import mock

import respx
from py_aws_core.clients import RetryClient

from src.layers.db_service import DatabaseService
from src.layers.testing import CSTestFixture
from src.layers.twocaptcha import api_twocaptcha, db_twocaptcha
from src.layers.twocaptcha.captcha_service import TwoCaptchaService


class TwoCaptchaImplTests(CSTestFixture):
    """
        Get Captcha ID Tests
    """

    @respx.mock
    @mock.patch.object(api_twocaptcha.SolveCaptcha, 'call')
    @mock.patch.object(api_twocaptcha.SolveCaptcha, 'get_webhook_url')
    @mock.patch.object(DatabaseService, 'update_captcha_event_on_solve_attempt')
    @mock.patch.object(DatabaseService, 'get_or_create_recaptcha_v2_event')
    def test_solve_captcha_ok(
        self,
        mocked_get_or_create_recaptcha_v2_event,
        mocked_update_captcha_event_on_solve_attempt,
        mocked_get_webhook_url,
        mocked_solve_captcha_call
    ):
        mocked_get_or_create_recaptcha_v2_event.return_value = 1
        mocked_update_captcha_event_on_solve_attempt.return_value = 1

        _json = self.get_api_resource_json('get_captcha_id.json')
        mocked_get_webhook_url.return_value = 'https://example.com/webhook'
        mocked_solve_captcha_call.return_value = api_twocaptcha.SolveCaptcha.Response(_json)

        with RetryClient() as client:
            captcha_service = TwoCaptchaService(db_service=DatabaseService())
            captcha_service.solve_captcha(
                http_client=client,
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com',
                webhook_url='https://ipsumlorem.com/webhook'
            )

        self.assertEqual(mocked_get_or_create_recaptcha_v2_event.call_count, 1)
        self.assertEqual(mocked_update_captcha_event_on_solve_attempt.call_count, 1)
        self.assertEqual(mocked_solve_captcha_call.call_count, 1)
        self.assertEqual(mocked_get_webhook_url.call_count, 1)

    @mock.patch.object(db_twocaptcha.CreateTCWebhookEvent, 'call')
    @mock.patch.object(DatabaseService, 'update_captcha_event_code')
    def test_handle_webhook_event_ok(
        self,
        mocked_update_captcha_event_code,
        mocked_create_tc_webhook_event_call
    ):
        mocked_update_captcha_event_code.return_value = True
        mocked_create_tc_webhook_event_call.return_value = True

        with RetryClient() as client:
            TwoCaptchaService(db_service=DatabaseService()).handle_webhook_event(
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

        with RetryClient() as client:
            webhook_data = {
                'test1': 'val1',
                'test33': 'ipsum lorem'
            }
            TwoCaptchaService(db_service=DatabaseService()).send_webhook_event(
                http_client=client,
                captcha_id='9991117777',
                captcha_token=self.TEST_RECAPTCHA_V2_TOKEN,
                webhook_url='http://mysite.com/pingback/url/',
                webhook_data=webhook_data,
            )

        self.assertEqual(mocked_post_webhook.call_count, 1)
        self.assertEqual(mocked_update_captcha_event_webhook.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_pingback_token')
    def test_get_verification_token_ok(
        self,
        mocked_get_pingback_token
    ):
        mocked_get_pingback_token.return_value = 'token123xyz'

        r = TwoCaptchaService.get_verification_token()

        self.assertEqual(r, 'token123xyz')
        self.assertEqual(mocked_get_pingback_token.call_count, 1)

    @mock.patch.object(db_twocaptcha.CreateTCCaptchaReport, 'call')
    @mock.patch.object(api_twocaptcha.ReportBadCaptcha, 'call')
    def test_report_bad_captcha_id_ok(
        self,
        mocked_report_bad_captcha,
        mocked_create_tc_captcha_report
    ):
        mocked_report_bad_captcha.return_value = True
        mocked_create_tc_captcha_report.return_value = True

        with RetryClient() as client:
            TwoCaptchaService.report_bad_captcha_id(
                http_client=client,
                captcha_id='9991117777'
            )

        self.assertEqual(mocked_report_bad_captcha.call_count, 1)
        self.assertEqual(mocked_create_tc_captcha_report.call_count, 1)

    @mock.patch.object(db_twocaptcha.CreateTCCaptchaReport, 'call')
    @mock.patch.object(api_twocaptcha.ReportGoodCaptcha, 'call')
    def test_report_good_captcha_id_ok(
        self,
        mocked_report_good_captcha,
        mocked_create_tc_captcha_report
    ):
        mocked_report_good_captcha.return_value = True
        mocked_create_tc_captcha_report.return_value = True

        with RetryClient() as client:
            TwoCaptchaService.report_good_captcha_id(
                http_client=client,
                captcha_id='9991117777'
            )

        self.assertEqual(mocked_report_good_captcha.call_count, 1)
        self.assertEqual(mocked_create_tc_captcha_report.call_count, 1)
