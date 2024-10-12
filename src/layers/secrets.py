from py_aws_core.ssm_parameter_store import get_secrets_manager

__secrets_manager = get_secrets_manager()


def get_app_name() -> str:
    return get_secret('APP_NAME')


def get_base_domain_name() -> str:
    return get_secret('BASE_DOMAIN_NAME')


def get_environment() -> str:
    return get_secret('ENVIRONMENT')


def get_captcha_password() -> str:
    return get_secret('CAPTCHA_PASSWORD')


def get_twocaptcha_pingback_token() -> str:
    return get_secret('TWOCAPTCHA_PINGBACK_TOKEN')


def get_secret(secret_name: str) -> str:
    return __secrets_manager.get_secret(secret_name)
