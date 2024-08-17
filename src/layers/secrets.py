from py_aws_core import secrets_manager

__sm = secrets_manager.get_secrets_manager()


def get_webhook_url() -> str:
    return f'{get_domain_name()}/pingback-event'


def get_domain_name() -> str:
    return __sm.get_secret(secret_name='DOMAIN_NAME')


