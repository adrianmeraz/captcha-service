from py_aws_core import utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events, logs
from src.layers.database import Database
from src.layers.i_captcha import ICaptcha
from src.layers.twocaptcha.captcha import TwoCaptcha

logger = logs.logger


def lambda_handler(event, context):
    logger.info(f'{__name__}, Incoming event: {event}')
    event = events.TwoCaptchaReportCaptchaEvent(event)
    captcha_service = TwoCaptcha(database=Database())
    process_event(event=event, captcha_service=captcha_service)
    return aws_utils.build_lambda_response(
        status_code=200,
        body={},
    )


def process_event(event: events.TwoCaptchaReportCaptchaEvent, captcha_service: ICaptcha):
    with RetryClient() as client:
        captcha_service.report_bad_captcha_id(http_client=client, captcha_id=event.captcha_id)
