from dataclasses import dataclass
from urllib.parse import urlencode

from py_aws_core.ssm_parameter_store import SSMParameterStore


@dataclass
class Secrets(SSMParameterStore):
    _app_name: str = None
    _base_domain_name: str = None
    _dynamo_db_table_name: str = None
    _environment: str = None
    _captcha_password: str = None
    _twocaptcha_pingback_token: str = None

    def get_webhook_url(self, params: dict = None) -> str:
        subdomain = f'{self.app_name}-{self.environment}'
        url = f'https://{subdomain}.{self.base_domain_name}/pingback-event'
        if params:
            url += f'?{urlencode(params)}'
        return url

    @property
    def app_name(self) -> str:
        return self._app_name or self.get_secret('APP_NAME')

    @property
    def base_domain_name(self) -> str:
        return self._base_domain_name or self.get_secret('BASE_DOMAIN_NAME')

    @property
    def dynamo_db_table_name(self) -> str:
        return self._dynamo_db_table_name or self.get_secret('AWS_DYNAMO_DB_TABLE_NAME')

    @property
    def environment(self) -> str:
        return self._environment or self.get_secret('ENVIRONMENT')

    @property
    def captcha_password(self) -> str:
        return self._captcha_password or self.get_secret('CAPTCHA_PASSWORD')

    @property
    def twocaptcha_pingback_token(self) -> str:
        return self._twocaptcha_pingback_token or self.get_secret('TWOCAPTCHA_PINGBACK_TOKEN')
