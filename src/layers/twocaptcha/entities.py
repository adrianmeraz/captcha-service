from py_aws_core.entities import ABCEntity


class TCWebhookEvent(ABCEntity):
    TYPE = 'TC_WEBHOOK_EVENT'

    def __init__(self, data):
        super().__init__(data)
        self.Id = self.data['Id']
        self.Code = self.data['Code']
        self.Rate = self.data['Rate']

    @classmethod
    def create_key(cls, _id: str) -> str:
        return f'{cls.type()}#{_id}'


class TCCaptchaReport(ABCEntity):
    TYPE = 'TC_CAPTCHA_REPORT'

    def __init__(self, data):
        super().__init__(data)
        self.Id = self.data['Id']
        self.Status = self.data['Status']

    @classmethod
    def create_key(cls, _id: str) -> str:
        return f'{cls.type()}#{_id}'
