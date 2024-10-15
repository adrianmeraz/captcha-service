import typing

from httpx import Client

from src.layers import logs, webhooks, exceptions, utils
from src.layers.captcha_interface import ICaptcha
from src.layers.db_interface import IDatabase
from src.layers.db_dynamo import const
from src.layers.twocaptcha import api_twocaptcha, exceptions as tc_exceptions
from src.layers.twocaptcha.db_interface import ITwoCaptchaDatabase

logger = logs.get_logger()


class CaptchaService(ICaptcha):
    def __init__(self, db_service: IDatabase | ITwoCaptchaDatabase):
        self._db_service = db_service

    def solve_captcha(
        self,
        http_client: Client,
        site_key: str,
        page_url: str,
        webhook_url: str,
        webhook_data: typing.Dict[str, str] = None,
        proxy_url: str = '',
        **kwargs
    ):
        request = api_twocaptcha.SolveCaptcha.Request(
            site_key=site_key,
            page_url=page_url,
            proxy_url=proxy_url,
            pingback_url=api_twocaptcha.SolveCaptcha.get_webhook_url(),
        )
        captcha_id = api_twocaptcha.SolveCaptcha.call(
            http_client=http_client,
            request=request
        ).request
        self._db_service.get_or_create_recaptcha_v2_event(
            captcha_id=captcha_id,
            page_url=page_url,
            proxy_url=proxy_url,
            site_key=site_key,
            webhook_url=webhook_url,
            webhook_data=webhook_data
        )
        self._db_service.update_captcha_event_on_solve_attempt(
            captcha_id=captcha_id
        )

    def handle_webhook_event(self, http_client: Client, captcha_id: str, code: str, rate: str, *args, **kwargs):
        self._db_service.create_webhook_event(
            captcha_id=captcha_id,
            code=code,
            rate=rate
        )
        if utils.is_valid_captcha_v2_token(captcha_token=code):
            status = const.CaptchaStatus.CAPTCHA_SOLVED
        else:
            status = const.CaptchaStatus.CAPTCHA_ERROR
        return self._db_service.update_captcha_event_code(
            captcha_id=captcha_id,
            code=code,
            status=status
        )

    def send_webhook_event(
        self,
        http_client: Client,
        captcha_id: str,
        captcha_token: str,
        webhook_url: str,
        webhook_data: typing.Dict[str, str] = None,
        *args,
        **kwargs
    ):
        if not webhook_data:
            webhook_data = dict()
        webhook_data |= {
            'captcha_id': captcha_id,
            'captcha_token': captcha_token,
        }
        if not utils.is_valid_captcha_v2_token(captcha_token):
            webhook_data['error'] = str(tc_exceptions.RESPONSE_EXCEPTION_MAP.get(captcha_token))

        try:
            request = webhooks.PostWebhook.Request(webhook_url=webhook_url, webhook_data=webhook_data)
            webhooks.PostWebhook.call(http_client=http_client, request=request)
            webhook_status = const.WebhookStatus.SUCCESS
        except exceptions.WebhookException:
            webhook_status = const.WebhookStatus.FAILED

        logger.info(f'Webhook url: {webhook_url}, data: {webhook_data}, status: {webhook_status.value}')
        self._db_service.update_captcha_event_webhook(
            captcha_id=captcha_id,
            webhook_status=webhook_status
        )

    @classmethod
    def get_verification_token(cls):
        return api_twocaptcha.TwoCaptchaAPI.get_pingback_token()

    def report_bad_captcha_id(self, http_client: Client, captcha_id: str, **kwargs):
        self._db_service.create_bad_captcha_report(captcha_id=captcha_id)
        request = api_twocaptcha.ReportBadCaptcha.Request(captcha_id=captcha_id)
        return api_twocaptcha.ReportBadCaptcha.call(http_client=http_client, request=request)

    def report_good_captcha_id(self, http_client: Client, captcha_id: str, **kwargs):
        self._db_service.create_good_captcha_report(_id=captcha_id)
        request = api_twocaptcha.ReportGoodCaptcha.Request(captcha_id=captcha_id)
        return api_twocaptcha.ReportGoodCaptcha.call(http_client=http_client, request=request)
