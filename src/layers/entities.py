from py_aws_core.entities import ABCEntity

from src.layers.const import EventCaptchaType


class CaptchaEvent(ABCEntity):
    TYPE = 'CAPTCHA_EVENT'

    @classmethod
    def create_key(cls, captcha_id: str, captcha_type: EventCaptchaType) -> str:
        return f'{cls.type()}#{captcha_type.value}#{captcha_id}'
