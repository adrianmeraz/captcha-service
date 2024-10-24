from py_aws_core.dynamodb_entities import ABCEntity


class TCWebhookEvent(ABCEntity):
    TYPE = 'TC_WEBHOOK_EVENT'

    def __init__(self, data: dict):
        super().__init__(data)
        self.Id = data['Id']
        self.Code = data['Code']
        self.Rate = data['Rate']

    @classmethod
    def create_key(cls, _id: str) -> str:
        return f'{cls.type()}#{_id}'


class TCCaptchaReport(ABCEntity):
    TYPE = 'TC_CAPTCHA_REPORT'

    def __init__(self, data: dict):
        super().__init__(data)
        self.Id = data['Id']
        self.Status = data['Status']

    @classmethod
    def create_key(cls, _id: str) -> str:
        return f'{cls.type()}#{_id}'
