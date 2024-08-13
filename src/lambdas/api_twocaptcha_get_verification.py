from py_aws_core import decorators, utils as aws_utils
from py_aws_core.spoofing.twocaptcha import twocaptcha_api

from src.layers import events, exceptions, logs

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CheckMigAPIException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    events.TwoCaptchaGetVerificationEvent(raw_event)
    return aws_utils.build_lambda_response(
        status_code=200,
        body=twocaptcha_api.TwoCaptchaAPI.get_pingback_token(),
    )
