import respx
from botocore.stub import Stubber
from py_aws_core.boto_clients import DynamoDBClientFactory, DynamoTableFactory
from src.lambdas import api_post_pingback_event
from src.layers.testing import CSTestFixture


class ApiPostPingbackEventTests(CSTestFixture):

    @respx.mock
    def test_ok(self):
        mock_event = self.get_event_resource_json('event#api_post_pingback_event.json')

        table = DynamoTableFactory.new_client(table_name='TEST_TABLE')
        stubber = Stubber(table.meta.client)

        put_item_json = self.get_db_resource_json('db#put_item.json')
        update_item_json = self.get_db_resource_json('db#update_captcha_event.json')
        stubber.add_response(method='put_item', service_response=put_item_json)
        stubber.add_response(method='update_item', service_response=update_item_json)
        stubber.add_response(method='update_item', service_response=update_item_json)
        stubber.activate()

        captcha_service = self.get_mock_captcha_service(table=table)

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

        stubber.assert_no_pending_responses()
