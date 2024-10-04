import typing
from abc import ABC, abstractmethod

from . import const, entities


class IDatabase(ABC):
    @classmethod
    @abstractmethod
    def get_or_create_recaptcha_v2_event(
        cls,
        captcha_id: str,
        page_url: str,
        site_key: str,
        webhook_data: typing.Dict[str, str],
        webhook_url: str,
        proxy_url: str = '',
        *args,
        **kwargs
    ) -> entities.CaptchaEvent:
        pass

    @classmethod
    @abstractmethod
    def update_captcha_event_code(
        cls,
        captcha_id: str,
        status: const.CaptchaStatus,
        code: str,
        *args,
        **kwargs
    ):
        pass

    @classmethod
    @abstractmethod
    def update_captcha_event_on_solve_attempt(
        cls,
        captcha_id: str,
        *args,
        **kwargs
    ):
        pass

    @classmethod
    @abstractmethod
    def update_captcha_event_webhook(
        cls,
        captcha_id: str,
        webhook_status: const.WebhookStatus,
        *args,
        **kwargs
    ):
        pass
