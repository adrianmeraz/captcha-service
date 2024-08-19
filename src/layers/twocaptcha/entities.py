import uuid

from py_aws_core.entities import ABCEntity


class RecaptchaEvent(ABCEntity):
    TYPE = 'RECAPTCHA_EVENT'

    @classmethod
    def create_key(cls, captcha_id: str) -> str:
        return f'{cls.type()}#{captcha_id}'
