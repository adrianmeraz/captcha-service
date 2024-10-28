from botocore.stub import Stubber
from py_aws_core.boto_clients import DynamoTable

from src.lambdas import api_get_pingback_verification_token
from src.layers.testing import CSTestFixture


class ApiGetPingbackVerificationTokenTests(CSTestFixture):
    def test_ok(self):
        mock_event = self.get_event_resource_json('event#api_get_pingback_verification_token.json')

        ddb_secrets = self.MockDynamoDBSecretsService()
        dynamo_table = DynamoTable(ddb_secrets=ddb_secrets)
        stubber = Stubber(dynamo_table.table.meta.client)
        stubber.activate()
        captcha_service = self.get_mocked_captcha_service(dynamo_table=dynamo_table)
        val = api_get_pingback_verification_token.lambda_handler(
            event=mock_event,
            context=None,
            captcha_service=captcha_service
        )
        self.assertEqual(
            val,
            {
                'body': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
                'multiValueHeaders': {
                    'Access-Control-Allow-Credentials': [True],
                    'Access-Control-Allow-Headers': ['Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'],
                    'Access-Control-Allow-Methods': ['DELETE,GET,POST,PUT'],
                    'Access-Control-Allow-Origin': ['*'],
                    'Content-Type': ['text/plain;charset=utf-8'],
                },
                'isBase64Encoded': False,
                'statusCode': 200
            }
        )
        stubber.assert_no_pending_responses()
