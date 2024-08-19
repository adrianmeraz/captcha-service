from unittest import TestCase

from src.layers import const, entities


class CaptchaEventTests(TestCase):
    def test_key(self):
        val = entities.CaptchaEvent.create_key(captcha_id='9991117777', captcha_type=const.EventCaptchaType.RECAPTCHA_V2)

        self.assertEqual(val, 'CAPTCHA_EVENT#RECAPTCHA_V2#9991117777')
