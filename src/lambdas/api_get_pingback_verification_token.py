from py_aws_core import decorators, utils as aws_utils

from src.layers import events, exceptions, logs
from src.layers.icaptcha import ICaptcha
from src.layers.twocaptcha.captcha import TwoCaptchaImpl

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    events.TwoCaptchaGetVerificationEvent(raw_event)
    response = process_event(captcha_service=TwoCaptchaImpl())
    return aws_utils.build_lambda_response(
        status_code=200,
        body=response,
        content_type='text/plain;charset=utf-8'
    )


def process_event(captcha_service: ICaptcha):
    return captcha_service.get_verification_token()
