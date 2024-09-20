from enum import Enum


class EventStatus(str, Enum):
    INIT = 'INIT'
    CAPTCHA_SOLVED = 'CAPTCHA_SOLVED'
    CAPTCHA_VALID = 'CAPTCHA_VALID'
    CAPTCHA_INVALID = 'CAPTCHA_INVALID'
    CAPTCHA_ERROR = 'CAPTCHA_ERROR'


class WebhookStatus(str, Enum):
    INIT = 'INIT'
    WEBHOOK_SUCCESS = 'WEBHOOK_SUCCESS'
    WEBHOOK_FAILED = 'WEBHOOK_FAILED'


class EventCaptchaType(str, Enum):
    RECAPTCHA_V2 = 'RECAPTCHA_V2'


PROXY_COUNTRY_WEIGHTS = [
    ('US', .70),
    ('CA', .12),
    ('UK', .12),
    ('AU', .06),
]
