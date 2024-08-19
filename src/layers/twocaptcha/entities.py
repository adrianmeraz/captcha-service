from py_aws_core.entities import ABCEntity

from .const import EventCaptchaType


class CaptchaEvent(ABCEntity):
    TYPE = 'RECAPTCHA_EVENT'

    @classmethod
    def create_key(cls, captcha_id: str, captcha_type: EventCaptchaType) -> str:
        return f'{cls.type()}#{captcha_type.value}#{captcha_id}'
