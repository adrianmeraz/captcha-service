from enum import Enum

DEFAULT_CAPTCHA_MAX_ATTEMPTS = 3
DEFAULT_WEBHOOK_MAX_ATTEMPTS = 3


class CaptchaStatus(str, Enum):
    INIT = 'INIT'
    CAPTCHA_SOLVED = 'CAPTCHA_SOLVED'
    CAPTCHA_VALID = 'CAPTCHA_VALID'
    CAPTCHA_INVALID = 'CAPTCHA_INVALID'
    CAPTCHA_ERROR = 'CAPTCHA_ERROR'
    CAPTCHA_SOLVING = 'CAPTCHA_SOLVING'


class WebhookStatus(str, Enum):
    INIT = 'INIT'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'


class EventCaptchaType(str, Enum):
    RECAPTCHA_V2 = 'RECAPTCHA_V2'


PROXY_COUNTRY_WEIGHTS = [
    ('US', .70),
    ('CA', .12),
    ('UK', .12),
    ('AU', .06),
]
