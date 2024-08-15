from py_aws_core import decorators, utils as aws_utils

from src.layers import events, exceptions, logs
from src.layers.twocaptcha.db_twocaptcha import TCDBAPI, get_db_client

logger = logs.logger
db_client = get_db_client()


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(raw_event, context):
    logger.info(f'{__name__}, Incoming event: {raw_event}')
    event = events.TwoCaptchaPostPingbackEvent(raw_event)
    process_event(event=event)
    return aws_utils.build_lambda_response(
        status_code=200,
        body='',
    )


def process_event(event: events.TwoCaptchaPostPingbackEvent):
    c_maps = [
        TCDBAPI.build_recaptcha_event_map(
            _id=event.id,
            code=event.code,
            params=event.params
        )
    ]
    db_client.write_maps_to_db(item_maps=c_maps)
    logger.info(f'Captcha Pingback Event written to database')
