from py_aws_core.events import LambdaEvent
from urllib.parse import parse_qs


class HttpEvent(LambdaEvent):
    pass


class TwoCaptchaGetVerificationEvent(HttpEvent):
    pass


class TwoCaptchaReportCaptchaEvent(HttpEvent):
    def __init__(self, data):
        super().__init__(data)
        self.captcha_id = self.body['captcha_id']


class TwoCaptchaPostPingbackEvent(HttpEvent):
    def __init__(self, data):
        super().__init__(data)
        self.query = parse_qs(self._body)
        self.code = self.query['code'][0]
        self.id = self.query['id'][0]
        self.rate = self.query['rate'][0]


class TwoCaptchaSolveCaptchaEvent(HttpEvent):
    def __init__(self, data):
        super().__init__(data)
        self.site_key = self.body['site_key']
        self.page_url = self.body['page_url']
        self.webhook_url = self.body['webhook_url']
        self.proxy_url = self.body.get('proxy_url')
        self.webhook_data = self.body.get('webhook_data')
