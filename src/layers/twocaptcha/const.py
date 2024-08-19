from enum import Enum


class EventStatus(str, Enum):
    INIT = 'INIT'
    CAPTCHA_SOLVED = 'CAPTCHA_SOLVED'
    CAPTCHA_VALID = 'CAPTCHA_VALID'
    CAPTCHA_INVALID = 'CAPTCHA_INVALID'
