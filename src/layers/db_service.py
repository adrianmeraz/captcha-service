from botocore.client import BaseClient

from . import const, dynamodb_api, entities
from .db_interface import IDatabase
from .secrets import Secrets
from .twocaptcha import tc_const, tc_db_dynamo
from .twocaptcha.db_interface import ITwoCaptchaDatabase


class DatabaseService(IDatabase, ITwoCaptchaDatabase):
    def __init__(self, boto_client: BaseClient, secrets: Secrets):
        self._boto_client = boto_client
        self._table_name = secrets.dynamo_db_table_name

    def get_or_create_recaptcha_v2_event(
        self,
        captcha_id: str,
        page_url: str,
        site_key: str,
        webhook_data: dict[str, str],
        webhook_url: str,
        proxy_url: str = '',
        *args,
        **kwargs
    ) -> entities.CaptchaEvent:
        return dynamodb_api.GetOrCreateRecaptchaV2Event.call(
            boto_client=self._boto_client,
            table_name=self._table_name,
            captcha_id=captcha_id,
            page_url=page_url,
            site_key=site_key,
            webhook_data=webhook_data,
            webhook_url=webhook_url,
            proxy_url=proxy_url
        ).captcha_event

    def update_captcha_event_code(
        self,
        captcha_id: str,
        status: const.CaptchaStatus,
        code: str,
        *args,
        **kwargs
    ):
        return dynamodb_api.UpdateCaptchaEventCode.call(
            boto_client=self._boto_client,
            table_name=self._table_name,
            captcha_id=captcha_id,
            status=status,
            code=code
        )

    def update_captcha_event_on_solve_attempt(
        self,
        captcha_id: str,
        *args,
        **kwargs
    ):
        return dynamodb_api.UpdateCaptchaEventOnSolveAttempt.call(
            boto_client=self._boto_client,
            table_name=self._table_name,
            captcha_id=captcha_id
        )

    def update_captcha_event_webhook(
        self,
        captcha_id: str,
        webhook_status: const.WebhookStatus,
        *args,
        **kwargs
    ):
        return dynamodb_api.UpdateCaptchaEventWebhook.call(
            boto_client=self._boto_client,
            table_name=self._table_name,
            captcha_id=captcha_id,
            webhook_status=webhook_status
        )

    def create_webhook_event(
        self,
        captcha_id: str,
        code: str,
        rate: str,
    ):
        tc_db_dynamo.CreateTCWebhookEvent.call(
            boto_client=self._boto_client,
            table_name=self._table_name,
            captcha_id=captcha_id,
            code=code,
            rate=rate
        )

    def create_captcha_report(
        self,
        captcha_id: str,
        status: tc_const.ReportStatus,
    ):
        tc_db_dynamo.CreateTCCaptchaReport.call(
            boto_client=self._boto_client,
            table_name=self._table_name,
            captcha_id=captcha_id,
            status=status
        )
