import typing

from httpx import Client

from src.layers import entities, logs
from src.layers.captcha import CaptchaInterface
from src.layers.twocaptcha import db_twocaptcha
from src.layers.twocaptcha.db_twocaptcha import const, get_db_client
from . import api_twocaptcha

logger = logs.logger
db_client = get_db_client()


class TwoCaptchaImpl(CaptchaInterface):
    @classmethod
    def solve_captcha(
        cls,
        client: Client,
        site_key: str,
        page_url: str,
        proxy_url: str = None,
        webhook_url: str = None,
        webhook_params: typing.Dict[str, str] = None,
        **kwargs
    ):
        request = api_twocaptcha.SolveCaptcha.Request(
            site_key=site_key,
            page_url=page_url,
            proxy_url=proxy_url,
            pingback_url=api_twocaptcha.SolveCaptcha.get_webhook_url(),
        )
        r = api_twocaptcha.SolveCaptcha.call(
            client=client,
            request=request
        )
        db_twocaptcha.CreateRecaptchaV2Event.call(
            db_client=db_client,
            captcha_id=r.request,
            webhook_url=webhook_url,
            webhook_params=webhook_params
        )

    @classmethod
    def handle_webhook_event(cls, captcha_id: str, code: str, *args, **kwargs):
        db_twocaptcha.UpdateCaptchaEvent.call(
            db_client=db_client,
            captcha_id=captcha_id,
            code=code,
            status=const.EventStatus.CAPTCHA_SOLVED
        )
        pk = entities.CaptchaEvent.create_key(captcha_id=captcha_id, captcha_type=const.EventCaptchaType.RECAPTCHA_V2)


    @classmethod
    def get_gcaptcha_token(cls, client: Client, captcha_id: int, **kwargs):
        return api_twocaptcha.GetSolvedToken.call(client=client, captcha_id=captcha_id)

    @classmethod
    def get_verification_token(cls):
        return api_twocaptcha.TwoCaptchaAPI.get_pingback_token()

    @classmethod
    def report_bad_captcha_id(cls, client: Client, captcha_id: int, **kwargs):
        return api_twocaptcha.ReportBadCaptcha.call(client=client, captcha_id=captcha_id)

    @classmethod
    def report_good_captcha_id(cls, client: Client, captcha_id: int, **kwargs):
        return api_twocaptcha.ReportGoodCaptcha.call(client=client, captcha_id=captcha_id)
