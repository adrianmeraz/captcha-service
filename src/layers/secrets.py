from urllib.parse import urlencode

from botocore.client import BaseClient
from py_aws_core.ssm_parameter_store import SSMParameterStore


class Secrets(SSMParameterStore):
    APP_NAME_KEY = 'APP_NAME'
    BASE_DOMAIN_NAME_KEY = 'BASE_DOMAIN_NAME'
    CAPTCHA_PASSWORD_KEY = 'CAPTCHA_PASSWORD'
    DYNAMO_TABLE_NAME_KEY = 'AWS_DYNAMO_DB_TABLE_NAME'
    ENVIRONMENT_KEY = 'ENVIRONMENT'
    TWOCAPTCHA_PINGBACK_TOKEN_KEY = 'TWOCAPTCHA_PINGBACK_TOKEN'

    def __init__(
        self,
        boto_client: BaseClient,
        app_name: str = None,
        base_domain_name: str = None,
        captcha_password: str = None,
        dynamo_db_table_name: str = None,
        environment: str = None,
        twocaptcha_pingback_token: str = None
    ):
        super().__init__(
            boto_client=boto_client,
            cached_secrets={
                self.APP_NAME_KEY: app_name,
                self.BASE_DOMAIN_NAME_KEY: base_domain_name,
                self.CAPTCHA_PASSWORD_KEY: captcha_password,
                self.DYNAMO_TABLE_NAME_KEY: dynamo_db_table_name,
                self.ENVIRONMENT_KEY: environment,
                self.TWOCAPTCHA_PINGBACK_TOKEN_KEY: twocaptcha_pingback_token
            }
        )

    def get_webhook_url(self, params: dict = None) -> str:
        subdomain = f'{self.app_name}-{self.environment}'
        url = f'https://{subdomain}.{self.base_domain_name}/pingback-event'
        if params:
            url += f'?{urlencode(params)}'
        return url

    @property
    def app_name(self) -> str:
        return self.get_secret(self.APP_NAME_KEY)

    @property
    def base_domain_name(self) -> str:
        return self.get_secret(self.BASE_DOMAIN_NAME_KEY)

    @property
    def captcha_password(self) -> str:
        return self.get_secret(self.CAPTCHA_PASSWORD_KEY)

    @property
    def dynamo_db_table_name(self) -> str:
        return self.get_secret(self.DYNAMO_TABLE_NAME_KEY)

    @property
    def environment(self) -> str:
        return self.get_secret(self.ENVIRONMENT_KEY)

    @property
    def twocaptcha_pingback_token(self) -> str:
        return self.get_secret(self.TWOCAPTCHA_PINGBACK_TOKEN_KEY)
