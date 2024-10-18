from unittest import mock

from py_aws_core.boto_clients import DynamoDBClientFactory

from src.lambdas import api_post_pingback_event
from src.layers.captcha_service import CaptchaService
from src.layers.db_service import DatabaseService
from src.layers.secrets import Secrets
from src.layers.testing import CSTestFixture


class ApiPostPingbackEventTests(CSTestFixture):

    @mock.patch.object(CaptchaService, 'send_webhook_event')
    @mock.patch.object(CaptchaService, 'handle_webhook_event')
    def test_ok(
        self,
        handle_webhook_event,
        send_webhook_event,
    ):
        mock_event = self.get_event_resource_json('event#api_post_pingback_event.json')

        handle_webhook_event.return_value = True
        send_webhook_event.return_value = True

        boto_client = DynamoDBClientFactory.new_client()
        secrets = Secrets(_dynamo_db_table_name='TEST_TABLE', _twocaptcha_pingback_token=self.TEST_VERIFICATION_TOKEN)
        db_service = DatabaseService(boto_client=boto_client, secrets=secrets)
        captcha_service = CaptchaService(db_service=db_service, secrets=secrets)

        val = api_post_pingback_event.lambda_handler(event=mock_event, context=None, captcha_service=captcha_service)
        self.maxDiff = None
        self.assertEqual(
            val,
            {
                'body': '{}',
                'multiValueHeaders': {
                    'Access-Control-Allow-Credentials': [True],
                    'Access-Control-Allow-Headers': ['Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'],
                    'Access-Control-Allow-Methods': ['DELETE,GET,POST,PUT'],
                    'Access-Control-Allow-Origin': ['*'],
                    'Content-Type': ['application/json'],
                },
                'isBase64Encoded': False,
                'statusCode': 200
            }
        )

        self.assertEqual(handle_webhook_event.call_count, 1)
        self.assertEqual(send_webhook_event.call_count, 1)
