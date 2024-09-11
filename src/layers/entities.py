from py_aws_core.entities import ABCEntity

from src.layers.const import EventCaptchaType


class CaptchaEvent(ABCEntity):
    TYPE = 'CAPTCHA_EVENT'

    def __init__(self, data):
        super().__init__(data)
        self.CaptchaId = self.data['CaptchaId']
        self.CaptchaType = self.data['CaptchaType']
        self.Code = self.data['Code']
        self.EventStatus = self.data['EventStatus']
        self.WebhookUrl = self.data['WebhookUrl']
        self.WebhookData = self.data['WebhookData']
        self.WebhookStatus = self.data['WebhookStatus']
        self.WebhookAttempts = self.data['WebhookAttempts']

    @classmethod
    def create_key(cls, captcha_id: str, captcha_type: EventCaptchaType) -> str:
        return f'{cls.type()}#{captcha_type.value}#{captcha_id}'
