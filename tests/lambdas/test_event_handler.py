import respx
from botocore.stub import Stubber
from py_aws_core.boto_clients import DynamoDBClientFactory

from src.lambdas import event_handler
from src.layers.testing import CSTestFixture


class EventHandlerTests(CSTestFixture):
    @respx.mock
    def test_routing_api_post_solve_captcha_event_ok(self):
        mock_event = self.get_event_resource_json('event#api_post_solve_captcha.json')

        boto_client = DynamoDBClientFactory.new_client()

        stubber_1 = Stubber(boto_client)
        update_item_json = self.get_db_resource_json('db#update_captcha_event.json')
        stubber_1.add_response(method='update_item', service_response=update_item_json)
        stubber_1.add_response(method='update_item', service_response=update_item_json)
        stubber_1.activate()

        mocked_solve_captcha = self.create_route(
            method='POST',
            url__eq='http://2captcha.com/in.php?key=test-password-1&method=userrecaptcha&googlekey=6LeN_osaAAAAAL-8U6H1IWdcFCY9kDBS34OBYqL_&pageurl=https%3A%2F%2Fapps.migracioncolombia.gov.co%2Fpre-registro%2Fes%2FDatosBiograficos&json=1&pingback=https%3A%2F%2Fbig-service-dev.ipsumlorem.com%2Fpingback-event',
            response_status_code=200,
            response_json=self.get_api_resource_json('get_captcha_id.json')
        )

        captcha_service = self.get_mock_captcha_service(boto_client=boto_client)

        val = event_handler.lambda_handler(event=mock_event, context=None, captcha_service=captcha_service)
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

        self.assertEqual(1, mocked_solve_captcha.call_count)
        stubber_1.assert_no_pending_responses()

    @respx.mock
    def test_routing_api_post_pingback_event_ok(self):
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
        val = event_handler.lambda_handler(event=mock_event, context=None, captcha_service=captcha_service)
        self.maxDiff = None
        self.assertEqual(
            val,
            {
                'body': '{}',
                'multiValueHeaders': {
                    'Access-Control-Allow-Credentials': [True],
                    'Access-Control-Allow-Headers': [
                        'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'],
                    'Access-Control-Allow-Methods': ['DELETE,GET,POST,PUT'],
                    'Access-Control-Allow-Origin': ['*'],
                    'Content-Type': ['application/json'],
                },
                'isBase64Encoded': False,
                'statusCode': 200
            }
        )

        stubber_1.assert_no_pending_responses()
