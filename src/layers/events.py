from py_aws_core.events import LambdaEvent


class HttpEvent(LambdaEvent):

    """
    TODO Maybe do some inspection of events here
    1. Linking person entities to em core travelers somehow.
    Could do this via local storage hashmaps
    Can expire the ids according to how long a checkmig session lasts
    """
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
        self.qs = self.query_string_parameters
        self.id = self.qs['id']
        self.code = self.qs['code']
        self.opt_data = self.qs['opt_data']


class TwoCaptchaSolveCaptchaEvent(HttpEvent):
    def __init__(self, data):
        super().__init__(data)
        self.site_key = self.body['site_key']
        self.page_url = self.body['page_url']
        self.webhook_url = self.body['webhook_url']
        self.opt_data = self.body.get('opt_data')
        self.proxy_url = self.body.get('proxy_url')
