from src.layers import const, entities
from src.layers.testing import CSTestFixture


class CaptchaEventTests(CSTestFixture):
    def test_key(self):
        key = entities.CaptchaEvent.create_key(captcha_id='9991117777', captcha_type=const.EventCaptchaType.RECAPTCHA_V2)

        self.assertEqual(key, 'CAPTCHA_EVENT#RECAPTCHA_V2#9991117777')

    def test_props(self):
        captcha_event = entities.CaptchaEvent(
            data={
                'CaptchaId': '9991117777',
                'CaptchaType': const.EventCaptchaType.RECAPTCHA_V2,
                'CaptchaAttempts': 3,
                'CaptchaMaxAttempts': 5,
                'Code': self.TEST_RECAPTCHA_V2_TOKEN,
                'EventStatus': const.EventStatus.CAPTCHA_INVALID,
                'PageUrl': 'https://example.com/captcha',
                'SiteKey': self.TEST_SITEKEY,
                'WebhookUrl': 'https://example.com/webhook',
                'WebhookData': {'key1': 'val1'},
                'WebhookStatus': const.WebhookStatus.INIT,
                'WebhookAttempts': 0,
            }
        )

        self.assertTrue(captcha_event.can_retry_captcha)
