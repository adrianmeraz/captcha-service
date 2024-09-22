import typing

from . import const, db_dynamo, entities
from .i_database import IDatabase

db_client = db_dynamo.get_db_client()


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
            db_client=db_client,
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
        return db_dynamo.UpdateCaptchaEventCode.call(
            db_client=db_client,
            captcha_id=captcha_id,
            status=status,
            code=code
        )

    @classmethod
    def update_captcha_event_on_solve_attempt(
        cls,
        captcha_id: str,
        *args,
        **kwargs
    ):
        return db_dynamo.UpdateCaptchaEventOnSolveAttempt.call(
            db_client=db_client,
            captcha_id=captcha_id
        )

    @classmethod
    def update_captcha_event_webhook(
        cls,
        captcha_id: str,
        webhook_status: const.WebhookStatus,
        *args,
        **kwargs
    ):
        return db_dynamo.UpdateCaptchaEventWebhook.call(
            db_client=db_client,
            captcha_id=captcha_id,
            webhook_status=webhook_status
        )
