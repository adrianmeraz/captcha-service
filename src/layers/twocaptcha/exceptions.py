from src.layers.exceptions import APIException


class TwoCaptchaException(APIException):
    ERROR_MESSAGE = 'A 2Captcha Error has occurred'


class WarnError(TwoCaptchaException):
    """2Captcha warn exception"""


class CriticalError(TwoCaptchaException):
    """2Captcha Critical exception"""


class CaptchaUnsolvable(TwoCaptchaException):
    """Captcha was unsolvable."""


class CaptchaNotReady(TwoCaptchaException):
    """Captcha is not Ready Yet"""


class InvalidResponse(TwoCaptchaException):
    """Response is not valid"""
