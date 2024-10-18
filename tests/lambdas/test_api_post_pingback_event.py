from botocore.stub import Stubber
from py_aws_core.boto_clients import DynamoDBClientFactory

from src.lambdas import api_post_pingback_event
from src.layers.testing import CSTestFixture


class ApiPostPingbackEventTests(CSTestFixture):

    def test_ok(self):
        mock_event = self.get_event_resource_json('event#api_post_pingback_event.json')

        boto_client = DynamoDBClientFactory.new_client()

        stubber_1 = Stubber(boto_client)
        put_item_json = self.get_db_resource_json('db#put_item.json')
        update_item_json = self.get_db_resource_json('db#update_captcha_event.json')
        stubber_1.add_response(method='put_item', service_response=put_item_json)
        stubber_1.add_response(method='update_item', service_response=update_item_json)
        stubber_1.add_response(method='update_item', service_response=update_item_json)
        stubber_1.activate()

        captcha_service = self.get_mock_captcha_service(boto_client=boto_client)

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

        stubber_1.assert_no_pending_responses()
