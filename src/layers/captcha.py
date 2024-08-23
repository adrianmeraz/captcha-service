import typing
from abc import ABC, abstractmethod

from httpx import Client


class CaptchaInterface(ABC):
    @classmethod
    @abstractmethod
    def solve_captcha(
        cls,
        http_client: Client,
        site_key: str,
        page_url: str,
        webhook_url: str,
        webhook_data: typing.Dict[str, str] = None,
        proxy_url: str = None,
        *args,
        **kwargs
    ):
        pass

    @classmethod
    @abstractmethod
    def handle_webhook_event(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def send_webhook_event(
        cls,
        http_client: Client,
        captcha_id: str,
        webhook_url: str,
        webhook_data: typing.Dict[str, str] = None,
        *args,
        **kwargs
    ):
        pass

    @classmethod
    @abstractmethod
    def get_verification_token(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def report_bad_captcha_id(cls, http_client: Client, captcha_id: str, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def report_good_captcha_id(cls, http_client: Client, captcha_id: str, *args, **kwargs):
        pass
