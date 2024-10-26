from py_aws_core.dynamodb_api import DynamoDBAPI

from src.layers import const, entities
from src.layers.testing import CSTestFixture


class CaptchaEventTests(CSTestFixture):
    def test_key(self):
        key = entities.CaptchaEvent.create_key(captcha_id='9991117777', captcha_type=const.EventCaptchaType.RECAPTCHA_V2)

        self.assertEqual(key, 'CAPTCHA_EVENT#RECAPTCHA_V2#9991117777')

    def test_props(self):
        _json = self.get_db_resource_json('db#update_captcha_event.json')

        deserialized_json = DynamoDBAPI.deserialize_types(_json['Attributes'])

        captcha_event = entities.CaptchaEvent(data=deserialized_json)

        self.assertTrue(captcha_event.can_retry_captcha)
        self.assertTrue(captcha_event.can_retry_webhook)
        self.assertFalse(captcha_event.has_captcha_error)
