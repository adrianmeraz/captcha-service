from functools import wraps

from .exceptions import CaptchaNotReady, CaptchaUnsolvable, CriticalError, InvalidResponse, WarnError

RESPONSE_EXCEPTION_MAP = {
    'ERROR_WRONG_CAPTCHA_ID': WarnError,
    'MAX_USER_TURN': WarnError,
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


def error_check(func):

    @wraps(func)
    def wrapper_func(*args, **kwargs):
        r = func(*args, **kwargs)
        if exc := RESPONSE_EXCEPTION_MAP.get(r.request):
            raise exc(*args, **kwargs)
        if r.status == 1:
            return r
        raise InvalidResponse(request=r.request, error_text=r.error_text)
    return wrapper_func
