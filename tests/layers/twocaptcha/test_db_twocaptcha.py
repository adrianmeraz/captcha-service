import json
from importlib.resources import as_file
from unittest import mock, TestCase

from botocore.exceptions import ClientError
from py_aws_core.db_dynamo import DDBClient

from src.layers.twocaptcha import const as tc_const, db_twocaptcha
from src.layers.twocaptcha.exceptions import DuplicateTCCaptchaReport, DuplicateTCWebhookEvent
from tests import const as test_const

RESOURCE_PATH = test_const.TEST_DB_RESOURCE_PATH


class CreateTCWebhookEventTests(TestCase):

    @mock.patch.object(DDBClient, 'put_item')
    def test_DuplicateTCWebhookEvent(
        self,
        mocked_put_item,
    ):
        source = RESOURCE_PATH.joinpath('errors', 'db#tc_webhook_event#duplicate_error.json')
        with as_file(source) as json_text:
            _json = json.loads(json_text.read_text(encoding='utf-8'))
            mocked_put_item.side_effect = ClientError(error_response=_json, operation_name='dummy')

        db_client = DDBClient()
        with self.assertRaises(DuplicateTCWebhookEvent):
            db_twocaptcha.CreateTCWebhookEvent.call(
                db_client=db_client,
                _id='77246411639',
                code='vmnurenvruejvv',
                rate='.00399'
            )

        self.assertEqual(mocked_put_item.call_count, 1)


class CreateTCCaptchaReportTests(TestCase):
    @mock.patch.object(DDBClient, 'put_item')
    def test_DuplicateTCCaptchaReport(
        self,
        mocked_put_item,
    ):
        source = RESOURCE_PATH.joinpath('errors', 'db#tc_webhook_event#duplicate_error.json')
        with as_file(source) as json_text:
            _json = json.loads(json_text.read_text(encoding='utf-8'))
            mocked_put_item.side_effect = ClientError(error_response=_json, operation_name='dummy')

        db_client = DDBClient()
        with self.assertRaises(DuplicateTCCaptchaReport):
            db_twocaptcha.CreateTCCaptchaReport.call(
                db_client=db_client,
                _id='77246411639',
                status=tc_const.ReportStatus.GOOD,
            )

        self.assertEqual(mocked_put_item.call_count, 1)
