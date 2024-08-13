import uuid

from py_aws_core.entities import ABCEntity


class RecaptchaEvent(ABCEntity):
    TYPE = 'RECAPTCHA_EVENT'

    @classmethod
    def create_key(cls, _id: uuid.UUID) -> str:
        return f'{cls.type()}#{_id}'
