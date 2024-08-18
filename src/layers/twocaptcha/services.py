import typing
import uuid

from httpx import Client

from src.layers import logs
from src.layers.interfaces import CaptchaInterface
from src.layers.twocaptcha.db_twocaptcha import TCDBAPI, get_db_client
from . import api_twocaptcha

logger = logs.logger
db_client = get_db_client()


class TwoCaptchaService(CaptchaInterface):
    @classmethod
    def solve_captcha(
        cls,
        client: Client,
        site_key: str,
        page_url: str,
        proxy_url: str = None,
        **kwargs
    ):
        request = api_twocaptcha.SolveCaptcha.Request(
            site_key=site_key,
            page_url=page_url,
            proxy_url=proxy_url,
            pingback_url=api_twocaptcha.SolveCaptcha.get_webhook_url(),
            opt_data=kwargs,
        )
        r = api_twocaptcha.SolveCaptcha.call(
            client=client,
            request=request
        )
        return r.request

    @classmethod
    def handle_webhook_event(cls, captcha_id: str, code: str, opt_data: typing.Dict, *args, **kwargs):
        c_maps = [
            TCDBAPI.build_recaptcha_event_map(
                _id=uuid.uuid4(),
                captcha_id=captcha_id,
                code=code,
                params=opt_data
            )
        ]
        db_client.write_maps_to_db(item_maps=c_maps)
        logger.info(f'Captcha Pingback Event written to database')

    @classmethod
    def get_gcaptcha_token(cls, client: Client, captcha_id: int, **kwargs):
        r = api_twocaptcha.GetSolvedToken.call(client=client, captcha_id=captcha_id)
        return r.request

    @classmethod
    def get_verification_token(cls):
        return api_twocaptcha.TwoCaptchaAPI.get_pingback_token()

    @classmethod
    def report_bad_captcha_id(cls, client: Client, captcha_id: int, **kwargs):
        return api_twocaptcha.ReportBadCaptcha.call(client=client, captcha_id=captcha_id)

    @classmethod
    def report_good_captcha_id(cls, client: Client, captcha_id: int, **kwargs):
        return api_twocaptcha.ReportGoodCaptcha.call(client=client, captcha_id=captcha_id)
