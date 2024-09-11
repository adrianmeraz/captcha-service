import json
from importlib.resources import as_file
from unittest import mock, TestCase

from py_aws_core.db_dynamo import DDBClient

from src.layers.twocaptcha import db_twocaptcha
from src.layers.twocaptcha.exceptions import DuplicateTCWebhookEvent
from tests import const as test_const

RESOURCE_PATH = test_const.TEST_DB_RESOURCE_PATH


class DBTwoCaptchaTests(TestCase):

    @mock.patch.object(DDBClient, 'put_item')
    def test_CreateTCWebhookEvent(
        self,
        mocked_put_item,
    ):
        source = RESOURCE_PATH.joinpath('errors', 'db#tc_webhook_event#duplicate_error.json')
        with as_file(source) as json_text:
            _json = json.loads(json_text.read_text(encoding='utf-8'))
            mocked_put_item.return_value = _json

        db_client = DDBClient()
        with self.assertRaises(DuplicateTCWebhookEvent):
            db_twocaptcha.CreateTCWebhookEvent.call(
                db_client=db_client,
                _id='77246411639',
                code='vmnurenvruejvv',
                rate='.00399'
            )

        self.assertEqual(mocked_put_item.call_count, 1)
