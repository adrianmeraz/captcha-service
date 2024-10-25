from botocore.stub import Stubber
from py_aws_core.boto_clients import DynamoTableFactory

from src.layers.testing import CSTestFixture
from src.layers.twocaptcha import tc_const as tc_const, tc_db_dynamo
from src.layers.twocaptcha.exceptions import DuplicateTCCaptchaReport, DuplicateTCWebhookEvent


class CreateTCWebhookEventTests(CSTestFixture):

    def test_DuplicateTCWebhookEvent(self):
        table = DynamoTableFactory.new_client(table_name='TEST_TABLE')
        stubber = Stubber(table.meta.client)
        stubber.add_client_error(method='put_item', service_error_code='ConditionalCheckFailedException')
        stubber.activate()

        with self.assertRaises(DuplicateTCWebhookEvent):
            tc_db_dynamo.CreateTCWebhookEvent.call(
                table=table,
                captcha_id='77246411639',
                code='vmnurenvruejvv',
                rate='.00399'
            )

        stubber.assert_no_pending_responses()


class CreateTCCaptchaReportTests(CSTestFixture):
    def test_DuplicateTCCaptchaReport(self):
        table = DynamoTableFactory.new_client(table_name='TEST_TABLE')

        stubber = Stubber(table.meta.client)
        stubber.add_client_error(method='put_item', service_error_code='ConditionalCheckFailedException')
        stubber.activate()

        with self.assertRaises(DuplicateTCCaptchaReport):
            tc_db_dynamo.CreateTCCaptchaReport.call(
                table=table,
                captcha_id='77246411639',
                status=tc_const.ReportStatus.GOOD,
            )

        stubber.assert_no_pending_responses()
