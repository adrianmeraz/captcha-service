from enum import Enum


class EventStatus(str, Enum):
    INIT = 'INIT'
    CAPTCHA_SOLVED = 'CAPTCHA_SOLVED'
    CAPTCHA_VALID = 'CAPTCHA_VALID'
    CAPTCHA_INVALID = 'CAPTCHA_INVALID'


class EventCaptchaType(str, Enum):
    RECAPTCHA_V2 = 'RECAPTCHA_V2'


PROXY_COUNTRY_WEIGHTS = [
    ('US', .70),
    ('CA', .12),
    ('UK', .12),
    ('AU', .06),
]
