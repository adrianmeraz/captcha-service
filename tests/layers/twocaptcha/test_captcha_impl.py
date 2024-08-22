import json
from importlib.resources import as_file
from unittest import mock

import respx
from py_aws_core.clients import RetryClient
from py_aws_core.db_dynamo import DDBClient
from py_aws_core.testing import BaseTestFixture

from src.layers.twocaptcha import api_twocaptcha
from src.layers.twocaptcha.captcha_impl import TwoCaptchaImpl
from tests import const as test_const

RESOURCE_PATH = test_const.TEST_API_RESOURCE_PATH


class TwoCaptchaImplTests(BaseTestFixture):
    """
        Get Captcha ID Tests
    """

    @respx.mock
    @mock.patch.object(DDBClient, 'batch_write_item_maps')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_environment')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_app_name')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_base_domain_name')
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
    def test_solve_captcha_ok(
        self,
        mocked_get_api_key,
        mocked_get_domain_name,
        mocked_get_app_name,
        mocked_get_environment,
        mocked_batch_write_item_maps
    ):
        mocked_get_api_key.return_value = 'IPSUMKEY'
        mocked_get_domain_name.return_value = 'ipsumlorem.com'
        mocked_get_app_name.return_value = 'big-service'
        mocked_get_environment.return_value = 'dev'
        mocked_batch_write_item_maps.return_value = 1

        source = RESOURCE_PATH.joinpath('get_captcha_id.json')
        with as_file(source) as warn_error_status_json:
            mocked_solve_captcha = self.create_route(
                method='POST',
                url__eq='http://2captcha.com/in.php?key=IPSUMKEY&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=https%3A%2F%2Fexample.com&json=1&pingback=https%3A%2F%2Fdev-big-service.ipsumlorem.com%2Fpingback-event',
                response_status_code=200,
                response_json=json.loads(warn_error_status_json.read_text(encoding='utf-8'))
            )

        with RetryClient() as client:
            TwoCaptchaImpl.solve_captcha(
                http_client=client,
                site_key='6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-',
                page_url='https://example.com',
                webhook_url='https://ipsumlorem.com/webhook'
            )


        self.assertEqual(mocked_get_api_key.call_count, 1)
        self.assertEqual(mocked_get_domain_name.call_count, 1)
        self.assertEqual(mocked_get_app_name.call_count, 1)
        self.assertEqual(mocked_get_environment.call_count, 1)
        self.assertEqual(mocked_solve_captcha.call_count, 1)
        self.assertEqual(mocked_batch_write_item_maps.call_count, 1)


# class GetSolvedCaptchaTests(BaseTestFixture):
#     """
#         Get Captcha ID Tests
#     """
#
#     @respx.mock
#     @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
#     def test_ok(self, mocked_get_api_key):
#         mocked_get_api_key.return_value = 'IPSUMKEY'
#
#         source = RESOURCE_PATH.joinpath('get_solved_token.json')
#         with as_file(source) as get_solved_token_json:
#             mocked_get_solved_token_route = self.create_ok_route(
#                 method='GET',
#                 url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=get&id=2122988149&json=1',
#                 _json=json.loads(get_solved_token_json.read_text(encoding='utf-8'))
#             )
#
#         with RetryClient() as client:
#             request = api_twocaptcha.GetSolvedToken.Request(captcha_id=2122988149)
#             r = api_twocaptcha.GetSolvedToken.call(
#                 client=client,
#                 request=request
#             )
#             self.assertEqual(r.request, '03AHJ_Vuve5Asa4koK3KSMyUkCq0vUFCR5Im4CwB7PzO3dCxIo11i53epEraq-uBO5mVm2XRikL8iKOWr0aG50sCuej9bXx5qcviUGSm4iK4NC_Q88flavWhaTXSh0VxoihBwBjXxwXuJZ-WGN5Sy4dtUl2wbpMqAj8Zwup1vyCaQJWFvRjYGWJ_TQBKTXNB5CCOgncqLetmJ6B6Cos7qoQyaB8ZzBOTGf5KSP6e-K9niYs772f53Oof6aJeSUDNjiKG9gN3FTrdwKwdnAwEYX-F37sI_vLB1Zs8NQo0PObHYy0b0sf7WSLkzzcIgW9GR0FwcCCm1P8lB-50GQHPEBJUHNnhJyDzwRoRAkVzrf7UkV8wKCdTwrrWqiYDgbrzURfHc2ESsp020MicJTasSiXmNRgryt-gf50q5BMkiRH7osm4DoUgsjc_XyQiEmQmxl5sqZP7aKsaE-EM00x59XsPzD3m3YI6SRCFRUevSyumBd7KmXE8VuzIO9lgnnbka4-eZynZa6vbB9cO3QjLH0xSG3-egcplD1uLGh79wC34RF49Ui3eHwua4S9XHpH6YBe7gXzz6_mv-o-fxrOuphwfrtwvvi2FGfpTexWvxhqWICMFTTjFBCEGEgj7_IFWEKirXW2RTZCVF0Gid7EtIsoEeZkPbrcUISGmgtiJkJ_KojuKwImF0G0CsTlxYTOU2sPsd5o1JDt65wGniQR2IZufnPbbK76Yh_KI2DY4cUxMfcb2fAXcFMc9dcpHg6f9wBXhUtFYTu6pi5LhhGuhpkiGcv6vWYNxMrpWJW_pV7q8mPilwkAP-zw5MJxkgijl2wDMpM-UUQ_k37FVtf-ndbQAIPG7S469doZMmb5IZYgvcB4ojqCW3Vz6Q')
#
#         self.assertEqual(mocked_get_api_key.call_count, 1)
#         self.assertEqual(mocked_get_solved_token_route.call_count, 1)
#
#     @respx.mock
#     @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_api_key')
#     def test_captcha_unsolvable(self, mocked_get_api_key):
#         mocked_get_api_key.return_value = 'IPSUMKEY'
#
#         source = RESOURCE_PATH.joinpath('captcha_unsolvable.json')
#         with as_file(source) as get_solved_token_json:
#             mocked_get_solved_token_route = self.create_ok_route(
#                 method='GET',
#                 url__eq='http://2captcha.com/res.php?key=IPSUMKEY&action=get&id=2122988149&json=1',
#                 _json=json.loads(get_solved_token_json.read_text(encoding='utf-8'))
#             )
#
#         with self.assertRaises(exceptions.CaptchaUnsolvable):
#             with RetryClient() as client:
#                 request = api_twocaptcha.GetSolvedToken.Request(captcha_id=2122988149)
#                 api_twocaptcha.GetSolvedToken.call(
#                     client=client,
#                     request=request
#                 )
#
#         self.assertEqual(mocked_get_api_key.call_count, 1)
#         self.assertEqual(mocked_get_solved_token_route.call_count, 1)
