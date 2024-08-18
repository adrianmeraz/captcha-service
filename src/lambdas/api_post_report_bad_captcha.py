from py_aws_core import decorators, utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events, exceptions, logs
from src.layers.interfaces import CaptchaInterface
from src.layers.twocaptcha.services import TwoCaptchaService

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = events.TwoCaptchaReportCaptchaEvent(raw_event)
    report_bad_captcha(event=event, captcha_service=TwoCaptchaService())
    return aws_utils.build_lambda_response(
        status_code=200,
        body={},
    )


def report_bad_captcha(event: events.TwoCaptchaReportCaptchaEvent, captcha_service: CaptchaInterface):
    with RetryClient() as client:
        captcha_service.report_bad_captcha_id(client=client, captcha_id=event.captcha_id)
