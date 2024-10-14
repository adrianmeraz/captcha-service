import typing

from httpx import Client

from src.layers import logs, webhooks, exceptions, utils
from src.layers.db_dynamo import const, get_db_client
from src.layers.i_captcha import ICaptcha
from src.layers.i_database import IDatabase
from . import api_twocaptcha, db_twocaptcha, exceptions as tc_exceptions, const as tc_const

logger = logs.get_logger()
db_client = get_db_client()


class TwoCaptchaService(ICaptcha):
    def __init__(self, db_service: IDatabase):
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
            db_client=db_client,
            captcha_id=captcha_id,
            page_url=page_url,
            proxy_url=proxy_url,
            site_key=site_key,
            webhook_url=webhook_url,
            webhook_data=webhook_data
        )
        self._db_service.update_captcha_event_on_solve_attempt(
            db_client=db_client,
            captcha_id=captcha_id
        )

    def handle_webhook_event(self, http_client: Client, captcha_id: str, code: str, rate: str, *args, **kwargs):
        db_twocaptcha.CreateTCWebhookEvent.call(
            db_client=db_client,
            _id=captcha_id,
            code=code,
            rate=rate
        )
        if utils.is_valid_captcha_v2_token(captcha_token=code):
            status = const.CaptchaStatus.CAPTCHA_SOLVED
        else:
            status = const.CaptchaStatus.CAPTCHA_ERROR
        return self._db_service.update_captcha_event_code(
            db_client=db_client,
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
            db_client=db_client,
            captcha_id=captcha_id,
            webhook_status=webhook_status
        )

    @classmethod
    def get_verification_token(cls):
        return api_twocaptcha.TwoCaptchaAPI.get_pingback_token()

    @classmethod
    def report_bad_captcha_id(cls, http_client: Client, captcha_id: str, **kwargs):
        db_twocaptcha.CreateTCCaptchaReport.call(db_client=db_client, _id=captcha_id, status=tc_const.ReportStatus.BAD)
        request = api_twocaptcha.ReportBadCaptcha.Request(captcha_id=captcha_id)
        return api_twocaptcha.ReportBadCaptcha.call(http_client=http_client, request=request)

    @classmethod
    def report_good_captcha_id(cls, http_client: Client, captcha_id: str, **kwargs):
        db_twocaptcha.CreateTCCaptchaReport.call(db_client=db_client, _id=captcha_id, status=tc_const.ReportStatus.GOOD)
        request = api_twocaptcha.ReportGoodCaptcha.Request(captcha_id=captcha_id)
        return api_twocaptcha.ReportGoodCaptcha.call(http_client=http_client, request=request)
