import logging
import random
import typing
from abc import ABC, abstractmethod

from httpx import Client
from py_aws_core.secrets_manager import get_secrets_manager

from . import const

logger = logging.getLogger(__name__)
secrets_manager = get_secrets_manager()


class ProxyInterface(ABC):
    @classmethod
    @abstractmethod
    def get_proxy_url(cls, **kwargs) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_weighted_country():
        countries, weights = zip(const.PROXY_COUNTRY_WEIGHTS)
        return random.choices(population=countries, weights=weights, k=1)[0]

    @classmethod
    @abstractmethod
    def get_proxy_password(cls):
        return secrets_manager.get_secret(secret_name='PROXY_PASSWORD')

    @classmethod
    @abstractmethod
    def get_proxy_username(cls):
        return secrets_manager.get_secret(secret_name='PROXY_USERNAME')


class CaptchaInterface(ABC):
    @classmethod
    @abstractmethod
    def solve_captcha(cls, client: Client, site_key: str, page_url: str, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def handle_webhook_event(cls, event: typing.Dict, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def get_gcaptcha_token(cls, client: Client, captcha_id: str, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def get_verification_token(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def report_bad_captcha_id(cls, client: Client, captcha_id: str, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def report_good_captcha_id(cls, client: Client, captcha_id: str, *args, **kwargs):
        pass
