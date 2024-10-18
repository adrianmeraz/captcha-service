from botocore.stub import Stubber
from py_aws_core.boto_clients import DynamoDBClientFactory

from src.layers.testing import CSTestFixture
from src.layers.twocaptcha import tc_const as tc_const, tc_db_dynamo
from src.layers.twocaptcha.exceptions import DuplicateTCCaptchaReport, DuplicateTCWebhookEvent


class CreateTCWebhookEventTests(CSTestFixture):

    def test_DuplicateTCWebhookEvent(self):
        _json = self.get_db_resource_json('errors', 'db#tc_webhook_event#duplicate_error.json')
        # mocked_put_item.side_effect = ClientError(error_response=_json, operation_name='dummy')

        boto_client = DynamoDBClientFactory.new_client()

        stubber = Stubber(boto_client)
        stubber.activate()
        stubber.add_client_error(method='put_item', service_error_meta=_json)
        # stubber.add_response(method='put_item', _json)

        with self.assertRaises(DuplicateTCWebhookEvent):
            tc_db_dynamo.CreateTCWebhookEvent.call(
                boto_client=boto_client,
                table_name='TEST_TABLE',
                captcha_id='77246411639',
                code='vmnurenvruejvv',
                rate='.00399'
            )


class CreateTCCaptchaReportTests(CSTestFixture):
    def test_DuplicateTCCaptchaReport(self):
        _json = self.get_db_resource_json('errors', 'db#tc_webhook_event#duplicate_error.json')
        # mocked_put_item.side_effect = ClientError(error_response=_json, operation_name='dummy')

        boto_client = DynamoDBClientFactory.new_client()

        stubber = Stubber(boto_client)
        stubber.activate()
        stubber.add_client_error(method='put_item', service_error_code='ConditionalCheckFailedException')

        with self.assertRaises(DuplicateTCCaptchaReport):
            tc_db_dynamo.CreateTCCaptchaReport.call(
                boto_client=boto_client,
                table_name='TEST_TABLE',
                captcha_id='77246411639',
                status=tc_const.ReportStatus.GOOD,
            )
