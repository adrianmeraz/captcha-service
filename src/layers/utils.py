import re


def is_valid_captcha_v2_token(captcha_token: str) -> bool:
    return re.match(r'[\w-]{500,1000}', captcha_token) is not None
