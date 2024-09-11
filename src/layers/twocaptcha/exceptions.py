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


class PingbackInvalidIP(TwoCaptchaException):
    """Pingback IP does not match IP of calling server"""


RESPONSE_EXCEPTION_MAP = {
    'ERROR_DUPLICATE_REPORT': WarnError,
    'ERROR_WRONG_CAPTCHA_ID': WarnError,
    'MAX_USER_TURN': WarnError,
    'ERROR_IP_ADDRES': PingbackInvalidIP,
    'ERROR_NO_SLOT_AVAILABLE': WarnError,
    'ERROR_PROXY_FORMAT': CriticalError,
    'ERROR_WRONG_USER_KEY': CriticalError,
    'ERROR_KEY_DOES_NOT_EXIST': CriticalError,
    'ERROR_ZERO_BALANCE': CriticalError,
    'IP_BANNED': CriticalError,
    'ERROR_GOOGLEKEY': CriticalError,
    'ERROR_CAPTCHA_UNSOLVABLE': CaptchaUnsolvable,
    'CAPCHA_NOT_READY':  CaptchaNotReady
}
