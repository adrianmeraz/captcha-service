from py_aws_core import utils as aws_utils

from src.layers import logs
from src.layers.database import Database
from src.layers.i_captcha import ICaptcha
from src.layers.routing import get_router
from src.layers.twocaptcha.captcha import TwoCaptcha

logger = logs.logger
apigw_router = get_router()


@apigw_router.route(path='/2captcha.txt', http_method='GET')
def lambda_handler(event, context):
    captcha_service = TwoCaptcha(database=Database())
    response = process_event(captcha_service=captcha_service)
    return aws_utils.build_lambda_response(
        status_code=200,
        body=response,
        content_type='text/plain;charset=utf-8'
    )


def process_event(captcha_service: ICaptcha):
    return captcha_service.get_verification_token()

