from unittest import mock

import respx
from py_aws_core.clients import RetryClient

from src.layers.testing import CSTestFixture
from src.layers.twocaptcha import api_twocaptcha, exceptions


class TwoCaptchaAPITests(CSTestFixture):
    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_environment')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_app_name')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_base_domain_name')
    def test_get_webhook_url_ok(
        self,
        mocked_get_domain_name,
        mocked_get_app_name,
        mocked_get_environment
    ):
        mocked_get_domain_name.return_value = 'ipsumlorem.com'
        mocked_get_app_name.return_value = 'big-service'
        mocked_get_environment.return_value = 'dev'

        params = {
            'ipsum_1': 'this is a test',
            'key2': 'value 456',
            'key3': 'xyzabc'
        }
        val = api_twocaptcha.TwoCaptchaAPI.get_webhook_url(params=params)
        self.assertEqual(val, 'https://big-service-dev.ipsumlorem.com/pingback-event?ipsum_1=this+is+a+test&key2=value+456&key3=xyzabc')

        self.assertEqual(mocked_get_domain_name.call_count, 1)
        self.assertEqual(mocked_get_app_name.call_count, 1)
        self.assertEqual(mocked_get_environment.call_count, 1)


class SolveCaptchaTests(CSTestFixture):
    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_ok(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_solve_captcha = self.create_ok_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
            _json=self.get_api_resource_json('get_captcha_id.json')
        )

        with RetryClient() as client:
            request = api_twocaptcha.SolveCaptcha.Request(
                proxy_url='http://example.com:1000',
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com',
            )
            r = api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)
        self.assertEqual(r.request, '2122988149')

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_redirect(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_solve_captcha = self.create_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
            response_status_code=301,
            response_json=self.get_api_resource_json('warn_error_status.json')
        )

        with self.assertRaises(exceptions.TwoCaptchaException):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_invalid_response(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_solve_captcha = self.create_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
            response_status_code=200,
            response_json=self.get_api_resource_json('warn_error_status.json')
        )

        with self.assertRaises(exceptions.InvalidCaptcha):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertTrue(mocked_solve_captcha.call_count, 1)
        self.assertTrue(mocked_get_api_key.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_warn_error(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_solve_captcha = self.create_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
            response_status_code=200,
            response_json={
                "status": 1,
                "request": "ERROR_WRONG_CAPTCHA_ID"
            }
        )

        with self.assertRaises(exceptions.TwoCaptchaException):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_critical_error(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_solve_captcha = self.create_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
            response_status_code=200,
            response_json={
                "status": 1,
                "request": "ERROR_WRONG_USER_KEY"
            }
        )

        with self.assertRaises(exceptions.CriticalError):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_captcha_unsolvable(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_solve_captcha = self.create_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
            response_status_code=200,
            response_json={
                "status": 1,
                "request": "ERROR_CAPTCHA_UNSOLVABLE"
            }
        )

        with self.assertRaises(exceptions.CaptchaUnsolvable):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_captcha_not_ready(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_solve_captcha = self.create_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
            response_status_code=200,
            response_json=self.get_api_resource_json('captcha_not_ready.json')
        )

        with self.assertRaises(exceptions.CaptchaNotReady):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)


class ReportCaptchaTests(CSTestFixture):
    """
        Report Captcha Tests
    """

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_reportbad_ok(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_report_bad_captcha = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportbad&id=2122988149&json=1',
            response_status_code=200,
            response_json=self.get_api_resource_json('report_captcha.json')
        )

        with RetryClient() as client:
            request = api_twocaptcha.ReportBadCaptcha.Request(captcha_id='2122988149')
            r_report = api_twocaptcha.ReportBadCaptcha.call(http_client=client, request=request)

        self.assertEqual(r_report.request, 'OK_REPORT_RECORDED')
        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_report_bad_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_reportgood_ok(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_report_good_captcha = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportgood&id=2122988149&json=1',
            response_status_code=200,
            response_json=self.get_api_resource_json('report_captcha.json')
        )

        with RetryClient() as client:
            request = api_twocaptcha.ReportGoodCaptcha.Request(captcha_id='2122988149')
            r_report = api_twocaptcha.ReportGoodCaptcha.call(http_client=client, request=request)

        self.assertEqual(r_report.request, 'OK_REPORT_RECORDED')
        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_report_good_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_reportbad_invalid_response(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_report_bad_captcha = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportbad&id=2122988149&json=1',
            response_status_code=200,
            response_json=self.get_api_resource_json('invalid_response.json')
        )

        with self.assertRaises(exceptions.InvalidResponse):
            with RetryClient() as client:
                request = api_twocaptcha.ReportBadCaptcha.Request(captcha_id='2122988149')
                api_twocaptcha.ReportBadCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_report_bad_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_invalid_report(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_report_bad_captcha = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportbad&id=2122988149&json=1',
            response_status_code=200,
            response_json=self.get_api_resource_json('warn_error_status.json')
        )

        with self.assertRaises(exceptions.InvalidCaptcha):
            with RetryClient() as client:
                request = api_twocaptcha.ReportBadCaptcha.Request(captcha_id='2122988149')
                api_twocaptcha.ReportBadCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_report_bad_captcha.call_count, 1)


class AddPingbackTests(CSTestFixture):
    """
        Add Pingback Tests
    """

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_ok(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_add_pingback = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=add_pingback&addr=http%3A%2F%2Fmysite.com%2Fpingback%2Furl%2F&json=1',
            response_status_code=200,
            response_json=self.get_api_resource_json('add_pingback.json')
        )

        with RetryClient() as client:
            request = api_twocaptcha.AddPingback.Request(pingback_url='http://mysite.com/pingback/url/')
            r_report = api_twocaptcha.AddPingback.call(
                http_client=client,
                request=request
            )

        self.assertEqual(r_report.request, 'OK_PINGBACK')

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_add_pingback.call_count, 1)
