from unittest import mock

import respx
from py_aws_core.clients import RetryClient

from src.layers.testing import CSTestFixture
from src.layers.twocaptcha import api_twocaptcha, exceptions


class SolveCaptchaTests(CSTestFixture):
    @respx.mock
    def test_ok(self):
        mocked_solve_captcha = self.create_ok_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
            _json=self.get_api_resource_json('get_captcha_id.json')
        )

        with RetryClient() as client:
            request = api_twocaptcha.SolveCaptcha.Request(
                api_key='IPSUMKEY',
                proxy_url='http://example.com:1000',
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com',
            )
            r = api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)
        self.assertEqual(r.request, '2122988149')

        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    def test_redirect(self):
        mocked_solve_captcha = self.create_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
            response_status_code=301,
            response_json=self.get_api_resource_json('warn_error_status.json')
        )

        with self.assertRaises(exceptions.TwoCaptchaException):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    api_key='IPSUMKEY',
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    def test_invalid_response(self):
        mocked_solve_captcha = self.create_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
            response_status_code=200,
            response_json=self.get_api_resource_json('warn_error_status.json')
        )

        with self.assertRaises(exceptions.InvalidCaptcha):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    api_key='IPSUMKEY',
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertTrue(mocked_solve_captcha.call_count, 1)

    @respx.mock
    def test_warn_error(self):
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
                    api_key='IPSUMKEY',
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    def test_critical_error(self):
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
                    api_key='IPSUMKEY',
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    def test_captcha_unsolvable(self,):
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
                    api_key='IPSUMKEY',
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    def test_captcha_not_ready(self):
        mocked_solve_captcha = self.create_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
            response_status_code=200,
            response_json=self.get_api_resource_json('captcha_not_ready.json')
        )

        with self.assertRaises(exceptions.CaptchaNotReady):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    api_key='IPSUMKEY',
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_solve_captcha.call_count, 1)


class ReportCaptchaTests(CSTestFixture):
    """
        Report Captcha Tests
    """

    @respx.mock
    def test_reportbad_ok(self):
        mocked_report_bad_captcha = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportbad&id=2122988149&json=1',
            response_status_code=200,
            response_json=self.get_api_resource_json('report_captcha.json')
        )

        with RetryClient() as client:
            request = api_twocaptcha.ReportBadCaptcha.Request(api_key='IPSUMKEY', captcha_id='2122988149')
            r_report = api_twocaptcha.ReportBadCaptcha.call(http_client=client, request=request)

        self.assertEqual(r_report.request, 'OK_REPORT_RECORDED')
        self.assertEqual(mocked_report_bad_captcha.call_count, 1)

    @respx.mock
    def test_reportgood_ok(self):
        mocked_report_good_captcha = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportgood&id=2122988149&json=1',
            response_status_code=200,
            response_json=self.get_api_resource_json('report_captcha.json')
        )

        with RetryClient() as client:
            request = api_twocaptcha.ReportGoodCaptcha.Request(api_key='IPSUMKEY', captcha_id='2122988149')
            r_report = api_twocaptcha.ReportGoodCaptcha.call(http_client=client, request=request)

        self.assertEqual(r_report.request, 'OK_REPORT_RECORDED')
        self.assertEqual(mocked_report_good_captcha.call_count, 1)

    @respx.mock
    def test_reportbad_invalid_response(self):
        mocked_report_bad_captcha = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportbad&id=2122988149&json=1',
            response_status_code=200,
            response_json=self.get_api_resource_json('invalid_response.json')
        )

        with self.assertRaises(exceptions.InvalidResponse):
            with RetryClient() as client:
                request = api_twocaptcha.ReportBadCaptcha.Request(api_key='IPSUMKEY', captcha_id='2122988149')
                api_twocaptcha.ReportBadCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_report_bad_captcha.call_count, 1)

    @respx.mock
    def test_invalid_report(self):
        mocked_report_bad_captcha = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportbad&id=2122988149&json=1',
            response_status_code=200,
            response_json=self.get_api_resource_json('warn_error_status.json')
        )

        with self.assertRaises(exceptions.InvalidCaptcha):
            with RetryClient() as client:
                request = api_twocaptcha.ReportBadCaptcha.Request(api_key='IPSUMKEY', captcha_id='2122988149')
                api_twocaptcha.ReportBadCaptcha.call(http_client=client, request=request)

        self.assertEqual(mocked_report_bad_captcha.call_count, 1)


class AddPingbackTests(CSTestFixture):
    """
        Add Pingback Tests
    """

    @respx.mock
    def test_ok(self):

        mocked_add_pingback = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=add_pingback&addr=http%3A%2F%2Fmysite.com%2Fpingback%2Furl%2F&json=1',
            response_status_code=200,
            response_json=self.get_api_resource_json('add_pingback.json')
        )

        with RetryClient() as client:
            request = api_twocaptcha.AddPingback.Request(
                api_key='IPSUMKEY',
                pingback_url='http://mysite.com/pingback/url/'
            )
            r_report = api_twocaptcha.AddPingback.call(
                http_client=client,
                request=request
            )

        self.assertEqual(r_report.request, 'OK_PINGBACK')

        self.assertEqual(mocked_add_pingback.call_count, 1)
