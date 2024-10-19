from py_aws_core.exceptions import CoreException


class CaptchaServiceException(CoreException):
    pass


class APIException(CaptchaServiceException):
    ERROR_MESSAGE = 'A generic API error occurred'


class WebhookException(CaptchaServiceException):
    ERROR_MESSAGE = 'A webhook error occurred'


class WebhookHttpStatusException(WebhookException):
    ERROR_MESSAGE = 'A webhook http status occurred'
