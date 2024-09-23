from src.layers import router
from . import (
    api_get_pingback_verification_token,
    api_post_pingback_event,
    api_post_report_bad_captcha,
    api_post_report_good_captcha,
    api_post_solve_captcha
)


apigw_router = router.APIGatewayRouter()

apigw_router.add_route(
    fn=api_get_pingback_verification_token.lambda_handler,
    http_method='GET',
    path='/2captcha.txt'
)
apigw_router.add_route(
    fn=api_post_pingback_event.lambda_handler,
    http_method='POST',
    path='/pingback-event'
)
apigw_router.add_route(
    fn=api_post_report_bad_captcha.lambda_handler,
    http_method='POST',
    path='/report-bad-captcha'
)
apigw_router.add_route(
    fn=api_post_report_good_captcha.lambda_handler,
    http_method='POST',
    path='/report-good-captcha'
)
apigw_router.add_route(
    fn=api_post_solve_captcha.lambda_handler,
    http_method='POST',
    path='/solve-captcha'
)
