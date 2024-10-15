from unittest import mock

from botocore.exceptions import ClientError
from src.layers.db_dynamo import DBClient

from src.layers.testing import CSTestFixture
from src.layers.twocaptcha import tc_const as tc_const, tc_db_dynamo
from src.layers.twocaptcha.exceptions import DuplicateTCCaptchaReport, DuplicateTCWebhookEvent


class CreateTCWebhookEventTests(CSTestFixture):

    @mock.patch.object(DBClient, 'put_item')
    def test_DuplicateTCWebhookEvent(
        self,
        mocked_put_item,
    ):
        _json = self.get_db_resource_json('errors', 'db#tc_webhook_event#duplicate_error.json')
        mocked_put_item.side_effect = ClientError(error_response=_json, operation_name='dummy')

        db_client = DBClient()
        with self.assertRaises(DuplicateTCWebhookEvent):
            tc_db_dynamo.CreateTCWebhookEvent.call(
                db_client=db_client,
                captcha_id='77246411639',
                code='vmnurenvruejvv',
                rate='.00399'
            )

        self.assertEqual(mocked_put_item.call_count, 1)


class CreateTCCaptchaReportTests(CSTestFixture):
    @mock.patch.object(DBClient, 'put_item')
    def test_DuplicateTCCaptchaReport(
        self,
        mocked_put_item,
    ):
        _json = self.get_db_resource_json('errors', 'db#tc_webhook_event#duplicate_error.json')
        mocked_put_item.side_effect = ClientError(error_response=_json, operation_name='dummy')

        db_client = DBClient()
        with self.assertRaises(DuplicateTCCaptchaReport):
            tc_db_dynamo.CreateTCCaptchaReport.call(
                db_client=db_client,
                captcha_id='77246411639',
                status=tc_const.ReportStatus.GOOD,
            )

        self.assertEqual(mocked_put_item.call_count, 1)
