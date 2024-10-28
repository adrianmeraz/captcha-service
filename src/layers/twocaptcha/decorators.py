from functools import wraps

from .exceptions import RESPONSE_EXCEPTION_MAP, InvalidResponse


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
