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


class TwoCaptchaAddPingbackEvent(HttpEvent):
    def __init__(self, data):
        super().__init__(data)
        self.pingback_url = self.body['pingback_url']


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
        self.params = self.qs['params']


class TwoCaptchaSolveCaptchaEvent(HttpEvent):
    def __init__(self, data):
        super().__init__(data)
        self.site_key = self.body['site_key']
        self.page_url = self.body['page_url']
        self.proxy_url = self.body.get('proxy_url')
        self.pingback = self.body.get('pingback')
