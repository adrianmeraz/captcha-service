from py_aws_core import decorators

from src.layers import exceptions
from src.layers.routing import get_router

apigw_router = get_router()


@decorators.lambda_response_handler(raise_as=exceptions.CaptchaServiceException)
def lambda_handler(event, context, **kwargs):
    return apigw_router.handle_event(aws_event=event, aws_context=context, **kwargs)
