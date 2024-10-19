import respx
from py_aws_core.clients import RetryClient

from src.layers import exceptions, webhooks
from src.layers.testing import CSTestFixture


class PostWebhookTests(CSTestFixture):
    """
        Post Webhook Tests
    """

    @respx.mock
    def test_ok(self):
        mocked_post_webhook = self.create_route(
            method='POST',
            url__eq='http://mysite.com/pingback/url/',
            response_status_code=200,
            response_text=''
        )

        with RetryClient() as client:
            webhook_data = {
                'test1': 'val1',
                'test33': 'ipsum lorem'
            }
            request = webhooks.PostWebhook.Request(
                webhook_url='http://mysite.com/pingback/url/',
                webhook_data=webhook_data
            )
            response = webhooks.PostWebhook.call(
                http_client=client,
                request=request
            )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(mocked_post_webhook.call_count, 1)

    @respx.mock
    def test_ok(self):
        mocked_post_webhook = self.create_route(
            method='POST',
            url__eq='http://mysite.com/pingback/url/',
            response_status_code=404,
            response_text=''
        )

        with self.assertRaises(exceptions.WebhookHttpStatusException):

            with RetryClient() as client:
                request = webhooks.PostWebhook.Request(
                    webhook_url='http://mysite.com/pingback/url/',
                    webhook_data=dict()
                )
                webhooks.PostWebhook.call(
                    http_client=client,
                    request=request
                )

        self.assertEqual(mocked_post_webhook.call_count, 1)
