class CaptchaServiceException(Exception):
    ERROR_MESSAGE = 'A generic error has occurred'

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.ERROR_MESSAGE

# Boto3 Exceptions Located below:
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html#botocore-exceptions
# https://github.com/boto/botocore/blob/develop/botocore/exceptions.py


class APIException(CaptchaServiceException):
    ERROR_MESSAGE = 'A generic API error occurred'


class WebhookException(CaptchaServiceException):
    ERROR_MESSAGE = 'A webhook error occurred'


class WebhookHttpStatusException(WebhookException):
    ERROR_MESSAGE = 'A webhook http status occurred'
