from dependency_injector.wiring import Provide, inject
from py_aws_core import utils as aws_utils
from py_aws_core.clients import RetryClient

from src.layers import events, logs
from src.layers.containers import Container
from src.layers.i_captcha import ICaptcha
from src.layers.routing import get_router

logger = logs.get_logger()
apigw_router = get_router()


@apigw_router.route(path='/report-bad-captcha', http_method='POST')
@inject
def lambda_handler(event, context, captcha_service: ICaptcha = Provide[Container.captcha_service]):
    event = events.CSReportCaptchaEvent(event)
    process_event(event=event, captcha_service=captcha_service)
    return aws_utils.build_lambda_response(
        status_code=200,
        body={},
    )


def process_event(event: events.CSReportCaptchaEvent, captcha_service: ICaptcha):
    with RetryClient() as client:
        captcha_service.report_bad_captcha_id(http_client=client, captcha_id=event.captcha_id)
