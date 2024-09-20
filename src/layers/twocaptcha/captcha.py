import typing

from httpx import Client

from src.layers import logs, webhooks, db_captcha, exceptions
from src.layers.db_captcha import const, get_db_client
from src.layers.interfaces import ICaptcha
from . import const as tc_const, api_twocaptcha, db_twocaptcha

logger = logs.logger
db_client = get_db_client()


class TwoCaptcha(ICaptcha):
    @classmethod
    def solve_captcha(
        cls,
        http_client: Client,
        site_key: str,
        page_url: str,
        webhook_url: str,
        webhook_data: typing.Dict[str, str] = None,
        proxy_url: str = None,
        **kwargs
    ):
        request = api_twocaptcha.SolveCaptcha.Request(
            site_key=site_key,
            page_url=page_url,
            proxy_url=proxy_url,
            pingback_url=api_twocaptcha.SolveCaptcha.get_webhook_url(),
        )
        r = api_twocaptcha.SolveCaptcha.call(
            http_client=http_client,
            request=request
        )
        db_captcha.CreateRecaptchaV2Event.call(
            db_client=db_client,
            captcha_id=r.request,
            webhook_url=webhook_url,
            webhook_data=webhook_data
        )

    @classmethod
    def handle_webhook_event(cls, http_client: Client, captcha_id: str, code: str, rate: str, *args, **kwargs):
        db_twocaptcha.CreateTCWebhookEvent.call(
            db_client=db_client,
            _id=captcha_id,
            code=code,
            rate=rate
        )
        return db_captcha.UpdateCaptchaEvent.call(
            db_client=db_client,
            captcha_id=captcha_id,
            code=code,
            status=const.EventStatus.CAPTCHA_SOLVED
        )

    @classmethod
    def send_webhook_event(
        cls,
        captcha_id: str,
        captcha_token: str,
        webhook_url: str,
        webhook_data: typing.Dict[str, str] = None,
        http_client: Client = None,
        *args,
        **kwargs
    ):
        if not webhook_data:
            webhook_data = dict()
        webhook_data |= {
            'captcha_id': captcha_id,
            'captcha_token': captcha_token,
        }
        request = webhooks.PostWebhook.Request(
            webhook_url=webhook_url,
            webhook_data=webhook_data
        )
        logger.info(f'{__name__}, Webhook details, webhook_url: {webhook_url}, webhook_data: {webhook_data}')

        try:
            webhooks.PostWebhook.call(http_client=http_client, request=request)
            webhook_status = const.WebhookStatus.WEBHOOK_SUCCESS
        except exceptions.WebhookException:
            webhook_status = const.WebhookStatus.WEBHOOK_FAILED

        logger.info(f'{__name__}, Webhook response status: {webhook_status.value}')
        db_captcha.UpdateCaptchaEventWebookStatus.call(
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
