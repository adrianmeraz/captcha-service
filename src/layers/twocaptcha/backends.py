from httpx import Client

from src.layers import secrets
from src.layers.backends import CaptchaService
from . import api_twocaptcha


class TwoCaptchaBackend(CaptchaService):
    def solve_captcha(
        self,
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
            pingback_url=secrets.get_webhook_url(),
        )
        r = api_twocaptcha.SolveCaptcha.call(
            client=client,
            request=request
        )
        return r.request

    def get_gcaptcha_token(self, client: Client, captcha_id: int, **kwargs):
        r = api_twocaptcha.GetSolvedToken.call(client=client, captcha_id=captcha_id)
        return r.request

    def report_bad_captcha_id(self, client: Client, captcha_id: int, **kwargs):
        return api_twocaptcha.ReportBadCaptcha.call(client=client, captcha_id=captcha_id)

    def report_good_captcha_id(self, client: Client, captcha_id: int, **kwargs):
        return api_twocaptcha.ReportGoodCaptcha.call(client=client, captcha_id=captcha_id)
