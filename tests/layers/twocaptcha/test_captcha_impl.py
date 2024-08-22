import json
from importlib.resources import as_file
from unittest import mock

import respx
from py_aws_core.clients import RetryClient
from py_aws_core.db_dynamo import DDBClient
from py_aws_core.testing import BaseTestFixture

from src.layers.twocaptcha import api_twocaptcha
from src.layers.twocaptcha import db_twocaptcha
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

    @mock.patch.object(db_twocaptcha.UpdateCaptchaEvent, 'call')
    def test_handle_webhook_event_ok(
        self,
        mocked_update_captcha_event_call
    ):
        mocked_update_captcha_event_call.return_value = True

        with RetryClient() as client:
            TwoCaptchaImpl.handle_webhook_event(
                http_client=client,
                captcha_id='9991117777',
                code='03AFcWeA5xt81X',
            )

        self.assertEqual(mocked_update_captcha_event_call.call_count, 1)

    @respx.mock
    @mock.patch.object(db_twocaptcha.UpdateCaptchaEventWebookStatus, 'call')
    def test_send_webhook_event_ok(
        self,
        mocked_update_captcha_event_webhook_status_call
    ):
        mocked_update_captcha_event_webhook_status_call.return_value = True

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
            TwoCaptchaImpl.send_webhook_event(
                http_client=client,
                captcha_id='9991117777',
                webhook_url='http://mysite.com/pingback/url/',
                webhook_data=webhook_data,
            )

        self.assertEqual(mocked_post_webhook.call_count, 1)
        self.assertEqual(mocked_update_captcha_event_webhook_status_call.call_count, 1)

    @respx.mock
    @mock.patch.object(api_twocaptcha.TwoCaptchaAPI, 'get_pingback_token')
    def test_get_verification_token_ok(
        self,
        mocked_get_pingback_token
    ):
        mocked_get_pingback_token.return_value = 'token123xyz'

        r = TwoCaptchaImpl.get_verification_token()

        self.assertEqual(r, 'token123xyz')
        self.assertEqual(mocked_get_pingback_token.call_count, 1)
