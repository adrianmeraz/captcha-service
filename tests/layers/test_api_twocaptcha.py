import json
from importlib.resources import as_file
from unittest import mock

import respx
from py_aws_core.clients import RetryClient
from py_aws_core.testing import BaseTestFixture

from src.layers.twocaptcha import api_twocaptcha, exceptions
from tests import const as test_const

RESOURCE_PATH = test_const.TEST_API_RESOURCE_PATH


class TwoCaptchaAPITests(BaseTestFixture):
    """
        Get Captcha ID Tests
    """

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_environment')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_app_name')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_base_domain_name')
    def test_ok(
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
        self.assertEqual(val, 'https://dev-big-service.ipsumlorem.com/pingback-event?ipsum_1=this+is+a+test&key2=value+456&key3=xyzabc')

        self.assertEqual(mocked_get_domain_name.call_count, 1)
        self.assertEqual(mocked_get_app_name.call_count, 1)
        self.assertEqual(mocked_get_environment.call_count, 1)


class GetSolvedCaptchaTests(BaseTestFixture):
    """
        Get Captcha ID Tests
    """

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_ok(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = RESOURCE_PATH.joinpath('get_solved_token.json')
        with as_file(source) as get_solved_token_json:
            mocked_get_solved_token_route = self.create_ok_route(
                method='GET',
                url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=get&id=2122988149&json=1',
                _json=json.loads(get_solved_token_json.read_text(encoding='utf-8'))
            )

        with RetryClient() as client:
            request = api_twocaptcha.GetSolvedToken.Request(captcha_id=2122988149)
            r = api_twocaptcha.GetSolvedToken.call(
                client=client,
                request=request
            )
            self.assertEqual(r.request, '03AHJ_Vuve5Asa4koK3KSMyUkCq0vUFCR5Im4CwB7PzO3dCxIo11i53epEraq-uBO5mVm2XRikL8iKOWr0aG50sCuej9bXx5qcviUGSm4iK4NC_Q88flavWhaTXSh0VxoihBwBjXxwXuJZ-WGN5Sy4dtUl2wbpMqAj8Zwup1vyCaQJWFvRjYGWJ_TQBKTXNB5CCOgncqLetmJ6B6Cos7qoQyaB8ZzBOTGf5KSP6e-K9niYs772f53Oof6aJeSUDNjiKG9gN3FTrdwKwdnAwEYX-F37sI_vLB1Zs8NQo0PObHYy0b0sf7WSLkzzcIgW9GR0FwcCCm1P8lB-50GQHPEBJUHNnhJyDzwRoRAkVzrf7UkV8wKCdTwrrWqiYDgbrzURfHc2ESsp020MicJTasSiXmNRgryt-gf50q5BMkiRH7osm4DoUgsjc_XyQiEmQmxl5sqZP7aKsaE-EM00x59XsPzD3m3YI6SRCFRUevSyumBd7KmXE8VuzIO9lgnnbka4-eZynZa6vbB9cO3QjLH0xSG3-egcplD1uLGh79wC34RF49Ui3eHwua4S9XHpH6YBe7gXzz6_mv-o-fxrOuphwfrtwvvi2FGfpTexWvxhqWICMFTTjFBCEGEgj7_IFWEKirXW2RTZCVF0Gid7EtIsoEeZkPbrcUISGmgtiJkJ_KojuKwImF0G0CsTlxYTOU2sPsd5o1JDt65wGniQR2IZufnPbbK76Yh_KI2DY4cUxMfcb2fAXcFMc9dcpHg6f9wBXhUtFYTu6pi5LhhGuhpkiGcv6vWYNxMrpWJW_pV7q8mPilwkAP-zw5MJxkgijl2wDMpM-UUQ_k37FVtf-ndbQAIPG7S469doZMmb5IZYgvcB4ojqCW3Vz6Q')

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_get_solved_token_route.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_captcha_unsolvable(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = RESOURCE_PATH.joinpath('captcha_unsolvable.json')
        with as_file(source) as get_solved_token_json:
            mocked_get_solved_token_route = self.create_ok_route(
                method='GET',
                url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=get&id=2122988149&json=1',
                _json=json.loads(get_solved_token_json.read_text(encoding='utf-8'))
            )

        with self.assertRaises(exceptions.CaptchaUnsolvable):
            with RetryClient() as client:
                request = api_twocaptcha.GetSolvedToken.Request(captcha_id=2122988149)
                api_twocaptcha.GetSolvedToken.call(
                    client=client,
                    request=request
                )

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_get_solved_token_route.call_count, 1)


class SolveCaptchaTests(BaseTestFixture):
    """
        Ping Captcha ID Tests
    """

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_ok(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = RESOURCE_PATH.joinpath('get_captcha_id.json')
        with as_file(source) as get_captcha_id_json:
            mocked_solve_captcha = self.create_ok_route(
                method='POST',
                url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
                _json=json.loads(get_captcha_id_json.read_text(encoding='utf-8'))
            )

        with RetryClient() as client:
            request = api_twocaptcha.SolveCaptcha.Request(
                proxy_url='http://example.com:1000',
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com',
            )
            r = api_twocaptcha.SolveCaptcha.call(client=client, request=request)
        self.assertEqual(r.request, '2122988149')

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_redirect(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = RESOURCE_PATH.joinpath('warn_error_status.json')
        with as_file(source) as warn_error_status_json:
            mocked_solve_captcha = self.create_route(
                method='POST',
                url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
                response_status_code=301,
                response_json=json.loads(warn_error_status_json.read_text(encoding='utf-8'))
            )

        with self.assertRaises(exceptions.TwoCaptchaException):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_invalid_response(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = RESOURCE_PATH.joinpath('warn_error_status.json')
        with as_file(source) as warn_error_status_json:
            mocked_solve_captcha = self.create_route(
                method='POST',
                url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
                response_status_code=200,
                response_json=json.loads(warn_error_status_json.read_text(encoding='utf-8'))
            )

        with self.assertRaises(exceptions.WarnError):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(client=client, request=request)

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
                api_twocaptcha.SolveCaptcha.call(client=client, request=request)

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
                api_twocaptcha.SolveCaptcha.call(client=client, request=request)

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
                api_twocaptcha.SolveCaptcha.call(client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_captcha_not_ready(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = RESOURCE_PATH.joinpath('captcha_not_ready.json')
        with as_file(source) as captcha_not_ready_json:
            mocked_solve_captcha = self.create_route(
                method='POST',
                url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&proxy=example.com%3A1000&proxytype=HTTP',
                response_status_code=200,
                response_json=json.loads(captcha_not_ready_json.read_text(encoding='utf-8'))
            )

        with self.assertRaises(exceptions.CaptchaNotReady):
            with RetryClient() as client:
                request = api_twocaptcha.SolveCaptcha.Request(
                    proxy_url='http://example.com:1000',
                    site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                    page_url='https://example.com',
                )
                api_twocaptcha.SolveCaptcha.call(client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)


class GetSolvedTokenTests(BaseTestFixture):
    """
        Get Solved Token Tests
    """

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_ok(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = RESOURCE_PATH.joinpath('get_solved_token.json')
        with as_file(source) as get_solved_token_json:
            mocked_get_solved_token = self.create_route(
                method='GET',
                url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=get&id=2122988149&json=1',
                response_status_code=200,
                response_json=json.loads(get_solved_token_json.read_text(encoding='utf-8'))
            )

        with RetryClient() as client:
            request = api_twocaptcha.GetSolvedToken.Request(captcha_id=2122988149)
            r = api_twocaptcha.GetSolvedToken.call(
                client=client,
                request=request,
            )

        self.assertEqual(r.request, '03AHJ_Vuve5Asa4koK3KSMyUkCq0vUFCR5Im4CwB7PzO3dCxIo11i53epEraq-uBO5mVm2XRikL8iKOWr0aG50sCuej9bXx5qcviUGSm4iK4NC_Q88flavWhaTXSh0VxoihBwBjXxwXuJZ-WGN5Sy4dtUl2wbpMqAj8Zwup1vyCaQJWFvRjYGWJ_TQBKTXNB5CCOgncqLetmJ6B6Cos7qoQyaB8ZzBOTGf5KSP6e-K9niYs772f53Oof6aJeSUDNjiKG9gN3FTrdwKwdnAwEYX-F37sI_vLB1Zs8NQo0PObHYy0b0sf7WSLkzzcIgW9GR0FwcCCm1P8lB-50GQHPEBJUHNnhJyDzwRoRAkVzrf7UkV8wKCdTwrrWqiYDgbrzURfHc2ESsp020MicJTasSiXmNRgryt-gf50q5BMkiRH7osm4DoUgsjc_XyQiEmQmxl5sqZP7aKsaE-EM00x59XsPzD3m3YI6SRCFRUevSyumBd7KmXE8VuzIO9lgnnbka4-eZynZa6vbB9cO3QjLH0xSG3-egcplD1uLGh79wC34RF49Ui3eHwua4S9XHpH6YBe7gXzz6_mv-o-fxrOuphwfrtwvvi2FGfpTexWvxhqWICMFTTjFBCEGEgj7_IFWEKirXW2RTZCVF0Gid7EtIsoEeZkPbrcUISGmgtiJkJ_KojuKwImF0G0CsTlxYTOU2sPsd5o1JDt65wGniQR2IZufnPbbK76Yh_KI2DY4cUxMfcb2fAXcFMc9dcpHg6f9wBXhUtFYTu6pi5LhhGuhpkiGcv6vWYNxMrpWJW_pV7q8mPilwkAP-zw5MJxkgijl2wDMpM-UUQ_k37FVtf-ndbQAIPG7S469doZMmb5IZYgvcB4ojqCW3Vz6Q')
        self.assertEqual(r.status, 1)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_get_solved_token.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_error_wrong_captcha_id(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        mocked_get_solved_token = self.create_route(
            method='GET',
            url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=get&id=2122988149&json=1',
            response_status_code=200,
            response_json={
                "status": 1,
                "request": "ERROR_WRONG_CAPTCHA_ID"
            }
        )

        with self.assertRaises(exceptions.WarnError):
            with RetryClient() as client:
                request = api_twocaptcha.GetSolvedToken.Request(captcha_id=2122988149)
                api_twocaptcha.GetSolvedToken.call(
                    client=client,
                    request=request
                )

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_get_solved_token.call_count, 1)


class ReportCaptchaTests(BaseTestFixture):
    """
        Report Captcha Tests
    """

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_reportbad_ok(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = RESOURCE_PATH.joinpath('report_captcha.json')
        with as_file(source) as report_captcha_json:
            mocked_report_bad_captcha = self.create_route(
                method='GET',
                url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportbad&id=2122988149&json=1',
                response_status_code=200,
                response_json=json.loads(report_captcha_json.read_text(encoding='utf-8'))
            )

        with RetryClient() as client:
            request = api_twocaptcha.ReportBadCaptcha.Request(captcha_id=2122988149)
            r_report = api_twocaptcha.ReportBadCaptcha.call(client=client, request=request)

        self.assertEqual(r_report.request, 'OK_REPORT_RECORDED')
        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_report_bad_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_reportgood_ok(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = RESOURCE_PATH.joinpath('report_captcha.json')
        with as_file(source) as report_captcha_json:
            mocked_report_good_captcha = self.create_route(
                method='GET',
                url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportgood&id=2122988149&json=1',
                response_status_code=200,
                response_json=json.loads(report_captcha_json.read_text(encoding='utf-8'))
            )

        with RetryClient() as client:
            request = api_twocaptcha.ReportGoodCaptcha.Request(captcha_id=2122988149)
            r_report = api_twocaptcha.ReportGoodCaptcha.call(client=client, request=request)

        self.assertEqual(r_report.request, 'OK_REPORT_RECORDED')
        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_report_good_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_reportbad_invalid_response(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = test_const.TEST_API_RESOURCE_PATH.joinpath('invalid_response.json')
        with as_file(source) as report_captcha_json:
            mocked_report_bad_captcha = self.create_route(
                method='GET',
                url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportbad&id=2122988149&json=1',
                response_status_code=200,
                response_json=json.loads(report_captcha_json.read_text(encoding='utf-8'))
            )

        with self.assertRaises(exceptions.InvalidResponse):
            with RetryClient() as client:
                request = api_twocaptcha.ReportBadCaptcha.Request(captcha_id=2122988149)
                api_twocaptcha.ReportBadCaptcha.call(client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_report_bad_captcha.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_invalid_report(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = test_const.TEST_API_RESOURCE_PATH.joinpath('warn_error_status.json')
        with as_file(source) as warn_error_status_json:
            mocked_report_bad_captcha = self.create_route(
                method='GET',
                url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=reportbad&id=2122988149&json=1',
                response_status_code=200,
                response_json=json.loads(warn_error_status_json.read_text(encoding='utf-8'))
            )

        with self.assertRaises(exceptions.WarnError):
            with RetryClient() as client:
                request = api_twocaptcha.ReportBadCaptcha.Request(captcha_id=2122988149)
                api_twocaptcha.ReportBadCaptcha.call(client=client, request=request)

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_report_bad_captcha.call_count, 1)


class AddPingbackTests(BaseTestFixture):
    """
        Add Pingback Tests
    """

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_ok(self, mocked_get_api_key):
        mocked_get_api_key.return_value = 'IPSUMKEY'

        source = test_const.TEST_API_RESOURCE_PATH.joinpath('add_pingback.json')
        with as_file(source) as warn_error_status_json:
            mocked_add_pingback = self.create_route(
                method='GET',
                url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=add_pingback&addr=http%3A%2F%2Fmysite.com%2Fpingback%2Furl%2F&json=1',
                response_status_code=200,
                response_json=json.loads(warn_error_status_json.read_text(encoding='utf-8'))
            )

        with RetryClient() as client:
            request = api_twocaptcha.AddPingback.Request(pingback_url='http://mysite.com/pingback/url/')
            r_report = api_twocaptcha.AddPingback.call(
                client=client,
                request=request
            )

        self.assertEqual(r_report.request, 'OK_PINGBACK')

        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_add_pingback.call_count, 1)
