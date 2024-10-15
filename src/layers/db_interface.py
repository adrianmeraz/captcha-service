import typing
from abc import ABC, abstractmethod

from . import const, entities


class IDatabase(ABC):
    @abstractmethod
    def get_or_create_recaptcha_v2_event(
        self,
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

    @abstractmethod
    def update_captcha_event_code(
        self,
        captcha_id: str,
        status: const.CaptchaStatus,
        code: str,
        *args,
        **kwargs
    ):
        pass

    @abstractmethod
    def update_captcha_event_on_solve_attempt(
        self,
        captcha_id: str,
        *args,
        **kwargs
    ):
        pass

    @abstractmethod
    def update_captcha_event_webhook(
        self,
        captcha_id: str,
        webhook_status: const.WebhookStatus,
        *args,
        **kwargs
    ):
        pass
