import typing
from urllib.parse import urlencode, urlparse

from httpx import Client
from py_aws_core import decorators as aws_decorators

from src.layers import logs
from src.layers.containers import Container
from . import decorators
from .exceptions import TwoCaptchaException

logger = logs.get_logger()


class TwoCaptchaAPI:
    ROOT_URL = 'http://2captcha.com'
    _container = Container()
    _secrets = _container.secrets

    @classmethod
    def get_api_key(cls) -> str:
        return cls._secrets.get_captcha_password()

    @classmethod
    def get_pingback_token(cls) -> str:
        return cls._secrets.get_twocaptcha_pingback_token()

    @classmethod
    def get_webhook_url(cls, params: typing.Dict = None) -> str:
        subdomain = f'{cls.get_app_name()}-{cls.get_environment()}'
        url = f'https://{subdomain}.{cls.get_base_domain_name()}/pingback-event'
        if params:
            url += f'?{urlencode(params)}'
        return url

    @classmethod
    def get_app_name(cls):
        return cls._secrets.get_app_name()

    @classmethod
    def get_base_domain_name(cls) -> str:
        return cls._secrets.get_base_domain_name()

    @classmethod
    def get_environment(cls) -> str:
        return cls._secrets.get_environment()


class TwoCaptchaResponse:
    def __init__(self, data):
        self.status = data['status']
        self.request = data['request']
        self.error_text = data.get('error_text')


class SolveCaptcha(TwoCaptchaAPI):
    class Request:
        def __init__(
            self,
            site_key: str,
            page_url: str,
            proxy_url: str = None,
            pingback_url: str = None,
            params: typing.Dict = None
        ):
            self.site_key = site_key
            self.page_url = page_url
            self.proxy_url = proxy_url
            self.pingback_url = pingback_url
            self.params = params

        @property
        def proxy(self) -> str | None:
            if self.proxy_url:
                return self.proxy_url_parts.netloc
            return None

        @property
        def proxy_type(self) -> str | None:
            if self.proxy_url:
                return self.proxy_url_parts.scheme.upper()
            return None

        @property
        def proxy_url_parts(self):
            if self.proxy_url:
                return urlparse(self.proxy_url)
            return None

    class Response(TwoCaptchaResponse):
        pass

    @classmethod
    @aws_decorators.wrap_exceptions(raise_as=TwoCaptchaException)
    @decorators.error_check
    def call(cls, http_client: Client, request: Request) -> Response:
        url = f'{cls.ROOT_URL}/in.php'

        params = {
            'key': cls.get_api_key(),
            'method': 'userrecaptcha',
            'googlekey': request.site_key,
            'pageurl': request.page_url,
            'json': '1',
        }
        if request.proxy_url:
            params |= {
                'proxy': request.proxy,
                'proxytype': request.proxy_type,
            }

        if request.pingback_url:
            params |= {
                'pingback': request.pingback_url
            }

        logger.info(f'Passing form data: {request.params}')
        r = http_client.post(url, params=params, follow_redirects=False)  # Disable redirects to network splash pages
        if not r.status_code == 200:
            raise TwoCaptchaException(f'Non 200 Response. Proxy: {request.proxy}, Response: {r.text}')

        return cls.Response(r.json())


class ReportCaptcha(TwoCaptchaAPI):
    class Request:
        def __init__(self, captcha_id: int, is_good: bool):
            self.captcha_id = captcha_id
            self.is_good = is_good

    class Response(TwoCaptchaResponse):
        pass

    @classmethod
    @aws_decorators.wrap_exceptions(raise_as=TwoCaptchaException)
    def call(cls, http_client: Client, request: Request) -> Response:
        url = f'{cls.ROOT_URL}/res.php'

        action = 'reportgood' if request.is_good else 'reportbad'

        params = {
            'key': cls.get_api_key(),
            'action': action,
            'id': request.captcha_id,
            'json': '1',
        }

        r = http_client.get(url, params=params)

        return cls.Response(r.json())


class ReportBadCaptcha(ReportCaptcha):
    class Request:
        def __init__(self, captcha_id: str):
            self.captcha_id = captcha_id
            self.is_good = False

    @classmethod
    @aws_decorators.wrap_exceptions(raise_as=TwoCaptchaException)
    @decorators.error_check
    def call(cls, http_client: Client, request: Request, **kwargs):
        r = super().call(http_client=http_client, request=request)
        logger.info(f'Reported bad captcha. id: {request.captcha_id}')
        return r


class ReportGoodCaptcha(ReportCaptcha):
    class Request:
        def __init__(self, captcha_id: str):
            self.captcha_id = captcha_id
            self.is_good = True

    @classmethod
    @aws_decorators.wrap_exceptions(raise_as=TwoCaptchaException)
    @decorators.error_check
    def call(cls, http_client: Client, request: Request, **kwargs):
        r = super().call(http_client=http_client, request=request)
        logger.info(f'Reported good captcha. id: {request.captcha_id}')
        return r


class AddPingback(TwoCaptchaAPI):
    class Request:
        def __init__(self, pingback_url: str):
            self.pingback_url = pingback_url

    class Response(TwoCaptchaResponse):
        pass

    @classmethod
    @aws_decorators.wrap_exceptions(raise_as=TwoCaptchaException)
    @decorators.error_check
    def call(cls, http_client: Client, request: Request) -> Response:
        url = f'{cls.ROOT_URL}/res.php'

        params = {
            'key': cls.get_api_key(),
            'action': 'add_pingback',
            'addr': request.pingback_url,
            'json': '1',
        }

        r = http_client.get(url, params=params)
        return cls.Response(r.json())
