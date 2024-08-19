from httpx import Client

from src.layers import const, logs
from src.layers.captcha import CaptchaInterface
from src.layers.twocaptcha.db_twocaptcha import const, TCDBAPI, get_db_client
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
        )
        r = api_twocaptcha.SolveCaptcha.call(
            client=client,
            request=request
        )
        captcha_id = r.request
        c_maps = [
            TCDBAPI.build_recaptcha_event_map(
                captcha_id=r.request,
                params=kwargs
            )
        ]
        db_client.write_maps_to_db(item_maps=c_maps)
        logger.info(f'{cls.__qualname__}, Captcha Pingback Event written to database, Captcha ID: {captcha_id}')

    @classmethod
    def handle_webhook_event(cls, captcha_id: str, code: str, *args, **kwargs):
        TCDBAPI.UpdateCaptchaEvent.call(
            db_client=db_client,
            captcha_id=captcha_id,
            status=const.EventStatus.CAPTCHA_SOLVED
        )
        logger.info(f'{cls.__qualname__}, Captcha Pingback Event updated, Captcha ID: {captcha_id}')

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
