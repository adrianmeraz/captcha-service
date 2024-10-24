from py_aws_core.dynamodb_entities import ABCEntity

from src.layers import const


class CaptchaEvent(ABCEntity):
    TYPE = 'CAPTCHA_EVENT'

    def __init__(self, data):
        super().__init__(data)
        self.CaptchaId = data['CaptchaId']
        self.CaptchaAttempts = data['CaptchaAttempts']
        self.CaptchaMaxAttempts = data['CaptchaMaxAttempts']
        self.CaptchaStatus = data['CaptchaStatus']
        self.CaptchaType = data['CaptchaType']
        self.Code = data['Code']
        self.PageUrl = data['PageUrl']
        self.ProxyUrl = data.get('ProxyUrl')
        self.SiteKey = data['SiteKey']
        self.WebhookUrl = data['WebhookUrl']
        self.WebhookData = data['WebhookData']
        self.WebhookStatus = data['WebhookStatus']
        self.WebhookAttempts = data['WebhookAttempts']
        self.WebhookMaxAttempts = data['WebhookMaxAttempts']

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
