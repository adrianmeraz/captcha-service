from py_aws_core.ssm_parameter_store import SSMParameterStore


class Secrets(SSMParameterStore):

    def get_app_name(self) -> str:
        return self.get_secret('APP_NAME')

    def get_base_domain_name(self) -> str:
        return self.get_secret('BASE_DOMAIN_NAME')

    def get_environment(self) -> str:
        return self.get_secret('ENVIRONMENT')

    def get_captcha_password(self) -> str:
        return self.get_secret('CAPTCHA_PASSWORD')

    def get_twocaptcha_pingback_token(self) -> str:
        return self.get_secret('TWOCAPTCHA_PINGBACK_TOKEN')
