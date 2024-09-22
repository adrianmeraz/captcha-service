import typing

from . import const, db_dynamo, entities
from .i_database import IDatabase


class Database(IDatabase):
    @classmethod
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
        return db_dynamo.GetOrCreateRecaptchaV2Event.call(
            captcha_id=captcha_id,
            page_url=page_url,
            site_key=site_key,
            webhook_data=webhook_data,
            webhook_url=webhook_url,
            proxy_url=proxy_url
        ).captcha_event

    @classmethod
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
    def update_captcha_event_on_solve_attempt(
        cls,
        captcha_id: str,
        *args,
        **kwargs
    ):
        pass

    @classmethod
    def update_captcha_event_webhook(
        cls,
        captcha_id: str,
        webhook_status: const.WebhookStatus,
        *args,
        **kwargs
    ):
        pass
