from py_aws_core import decorators, utils as aws_utils

from src.layers import events, exceptions, logs
from src.layers.twocaptcha import api_twocaptcha

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    events.TwoCaptchaGetVerificationEvent(raw_event)
    return aws_utils.build_lambda_response(
        status_code=200,
        body=get_pingback_verification_token()
    )


def get_pingback_verification_token():
    return api_twocaptcha.TwoCaptchaAPI.get_pingback_token()
