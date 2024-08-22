import typing

from httpx import Client
from py_aws_core import decorators as aws_decorators

from .exceptions import WebhookException, WebhookHttpStatusException


class PostWebhook:
    class Request:
        def __init__(self, webhook_url: str, webhook_data: typing.Dict = None):
            self.webhook_url = webhook_url
            self.webhook_data = webhook_data or dict()

    @classmethod
    @aws_decorators.wrap_exceptions(raise_as=WebhookException)
    def call(cls, http_client: Client, request: Request):
        url = request.webhook_url
        r = http_client.post(url, data=request.webhook_data)
        if not r.is_success:
            raise WebhookHttpStatusException(r.status_code)
        return r
