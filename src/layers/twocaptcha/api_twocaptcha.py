import logging
import typing
from urllib.parse import urlencode, urlparse

from httpx import Client
from py_aws_core import decorators as aws_decorators
from py_aws_core.secrets_manager import get_secrets_manager

from . import decorators
from .exceptions import CaptchaNotReady, TwoCaptchaException

logger = logging.getLogger(__name__)
secrets_manager = get_secrets_manager()


class TwoCaptchaAPI:
    ROOT_URL = 'http://2captcha.com'

    @classmethod
    def get_api_key(cls) -> str:
        return secrets_manager.get_secret('CAPTCHA_PASSWORD')

    @classmethod
    def get_pingback_token(cls) -> str:
        return secrets_manager.get_secret('TWOCAPTCHA_PINGBACK_TOKEN')

    @classmethod
    def get_webhook_url(cls, params: typing.Dict = None) -> str:
        subdomain = f'{cls.get_environment()}-{cls.get_app_name()}'
        url = f'https://{subdomain}.{cls.get_base_domain_name()}/pingback-event'
        if params:
            url += f'?{urlencode(params)}'
        return url

    @classmethod
    def get_app_name(cls):
        return secrets_manager.get_secret(secret_name='APP_NAME')

    @classmethod
    def get_base_domain_name(cls) -> str:
        return secrets_manager.get_secret(secret_name='BASE_DOMAIN_NAME')

    @classmethod
    def get_environment(cls) -> str:
        return secrets_manager.get_secret(secret_name='ENVIRONMENT')


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

        logger.info(f'{__name__}.{cls.__qualname__}.call#, Passing form data: {request.params}')
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
        def __init__(self, captcha_id: int):
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
        def __init__(self, captcha_id: int):
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
