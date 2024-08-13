import logging
from urllib.parse import urlparse

from httpx import Client

from py_aws_core import decorators as aws_decorators
from py_aws_core.secrets_manager import get_secrets_manager
from . import decorators
from .exceptions import CaptchaNotReady, TwoCaptchaException

logger = logging.getLogger(__name__)
secrets_manager = get_secrets_manager()


class TwoCaptchaAPI:
    _api_key = None
    ROOT_URL = 'http://2captcha.com'

    @classmethod
    def get_api_key(cls):
        if not cls._api_key:
            cls._api_key = secrets_manager.get_secret('CAPTCHA_PASSWORD')
        return cls._api_key

    @classmethod
    def get_pingback_token(cls):
        if not cls._api_key:
            cls._api_key = secrets_manager.get_secret('TWOCAPTCHA_PINGBACK_TOKEN')
        return cls._api_key


class TwoCaptchaResponse:
    def __init__(self, data):
        self.status = data['status']
        self.request = data['request']
        self.error_text = data.get('error_text')

    @property
    def is_captcha_reported(self):
        return self.request == 'OK_REPORT_RECORDED'


class PingCaptchaId(TwoCaptchaAPI):
    class Request:
        def __init__(self, site_key: str, page_url: str, proxy_url: str = None, pingback: str = None):
            self.proxy_url = proxy_url
            self.site_key = site_key
            self.page_url = page_url
            self.pingback = pingback

        @property
        def proxy(self) -> str:
            return self.proxy_url_parts.netloc

        @property
        def proxy_type(self) -> str:
            return self.proxy_url_parts.scheme.upper()

        @property
        def proxy_url_parts(self):
            return urlparse(self.proxy_url)

    class Response(TwoCaptchaResponse):
        pass

    @classmethod
    @decorators.error_check
    def call(cls, client: Client, request: Request) -> Response:
        url = f'{cls.ROOT_URL}/in.php'

        params = {
            'key': cls.get_api_key(),
            'method': 'userrecaptcha',
            'googlekey': request.site_key,
            'pageurl': request.page_url,
            'json': '1',
            'proxy': request.proxy,
            'proxytype': request.proxy_type,
        }
        if request.pingback:
            params['pingback'] = request.pingback

        r = client.post(url, params=params, follow_redirects=False)  # Disable redirects to network splash pages
        if not r.status_code == 200:
            raise TwoCaptchaException(f'Non 200 Response. Proxy: {request.proxy}, Response: {r.text}')

        return cls.Response(r.json())


class GetSolvedToken(TwoCaptchaAPI):
    class Response(TwoCaptchaResponse):
        pass

    @classmethod
    @aws_decorators.retry(retry_exceptions=(CaptchaNotReady,), tries=60, delay=5, backoff=1)
    @decorators.error_check
    def call(cls, client: Client, captcha_id: int) -> Response:
        url = f'{cls.ROOT_URL}/res.php'

        params = {
            'key': cls.get_api_key(),
            'action': 'get',
            'id': captcha_id,
            'json': 1,
        }

        r = client.get(url, params=params)

        return cls.Response(r.json())


class ReportCaptcha(TwoCaptchaAPI):
    class Response(TwoCaptchaResponse):
        pass

    @classmethod
    def call(cls, client: Client, captcha_id: int, is_good: bool) -> Response:
        url = f'{cls.ROOT_URL}/res.php'

        action = 'reportgood' if is_good else 'reportbad'

        params = {
            'key': cls.get_api_key(),
            'action': action,
            'id': captcha_id,
            'json': '1',
        }

        r = client.get(url, params=params)

        return cls.Response(r.json())


class ReportBadCaptcha(ReportCaptcha):
    @classmethod
    @decorators.error_check
    def call(cls, client: Client, captcha_id: int, **kwargs):
        r = super().call(client=client, captcha_id=captcha_id, is_good=False)
        logger.info(f'Reported bad captcha. id: {captcha_id}')
        return r


class ReportGoodCaptcha(ReportCaptcha):
    @classmethod
    @decorators.error_check
    def call(cls, client: Client, captcha_id: int, **kwargs):
        r = super().call(client=client, captcha_id=captcha_id, is_good=True)
        logger.info(f'Reported good captcha. id: {captcha_id}')
        return r


class AddPingback(TwoCaptchaAPI):
    class Response(TwoCaptchaResponse):
        pass

    @classmethod
    @aws_decorators.retry(retry_exceptions=(CaptchaNotReady,))
    @decorators.error_check
    def call(cls, client: Client, addr: str) -> Response:
        url = f'{cls.ROOT_URL}/res.php'

        params = {
            'key': cls.get_api_key(),
            'action': 'add_pingback',
            'addr': addr,
            'json': '1',
        }

        r = client.get(url, params=params)
        return cls.Response(r.json())

