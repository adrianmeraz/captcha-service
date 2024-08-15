from py_aws_core import decorators, utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events, exceptions, logs
from src.layers.twocaptcha import api_twocaptcha

logger = logs.logger


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = events.TwoCaptchaReportCaptchaEvent(raw_event)
    report_good_captcha(event=event)
    return aws_utils.build_lambda_response(
        status_code=200,
        body={},
    )


def report_good_captcha(event: events.TwoCaptchaReportCaptchaEvent):
    with RetryClient() as client:
        request = api_twocaptcha.ReportGoodCaptcha.Request(captcha_id=event.captcha_id)
        api_twocaptcha.ReportGoodCaptcha.call(client=client, request=request)
