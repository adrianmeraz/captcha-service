from httpx import Client

from py_aws_core.spoofing.backends import CaptchaBackend
from . import api_twocaptcha


class TwoCaptchaBackend(CaptchaBackend):
    def get_captcha_id(self, client: Client, site_key: str, page_url: str, proxy: str = None, **kwargs):
        r = api_twocaptcha.SolveCaptcha.call(
            client=client,
            proxy=proxy,
            site_key=site_key,
            page_url=page_url
        )
        return r.request

    def get_gcaptcha_token(self, client: Client, captcha_id: int, **kwargs):
        r = api_twocaptcha.GetSolvedToken.call(client=client, captcha_id=captcha_id)
        return r.request

    def report_bad_captcha_id(self, client: Client, captcha_id: int, **kwargs):
        return api_twocaptcha.ReportBadCaptcha.call(client=client, captcha_id=captcha_id)

    def report_good_captcha_id(self, client: Client, captcha_id: int, **kwargs):
        return api_twocaptcha.ReportGoodCaptcha.call(client=client, captcha_id=captcha_id)
