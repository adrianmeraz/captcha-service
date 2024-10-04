from py_aws_core.entities import ABCEntity

from src.layers import const


class CaptchaEvent(ABCEntity):
    TYPE = 'CAPTCHA_EVENT'

    def __init__(self, data):
        super().__init__(data)
        self.CaptchaId = self.data['CaptchaId']
        self.CaptchaAttempts = self.data['CaptchaAttempts']
        self.CaptchaMaxAttempts = self.data['CaptchaMaxAttempts']
        self.CaptchaStatus = self.data['CaptchaStatus']
        self.CaptchaType = self.data['CaptchaType']
        self.Code = self.data['Code']
        self.PageUrl = self.data['PageUrl']
        self.ProxyUrl = self.data.get('ProxyUrl')
        self.SiteKey = self.data['SiteKey']
        self.WebhookUrl = self.data['WebhookUrl']
        self.WebhookData = self.data['WebhookData']
        self.WebhookStatus = self.data['WebhookStatus']
        self.WebhookAttempts = self.data['WebhookAttempts']
        self.WebhookMaxAttempts = self.data['WebhookMaxAttempts']

    @classmethod
    def create_key(cls, captcha_id: str, captcha_type: const.EventCaptchaType) -> str:
        return f'{cls.type()}#{captcha_type.value}#{captcha_id}'

    @property
    def has_captcha_error(self) -> bool:
        return self.CaptchaStatus == const.CaptchaStatus.CAPTCHA_ERROR.value

    @property
    def can_retry_captcha(self):
        return self.CaptchaAttempts < self.CaptchaMaxAttempts

    @property
    def can_retry_webhook(self):
        return self.WebhookAttempts < self.WebhookMaxAttempts
