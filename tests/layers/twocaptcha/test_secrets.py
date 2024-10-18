from src.layers.secrets import Secrets
from src.layers.testing import CSTestFixture


class SecretsTests(CSTestFixture):
    def test_get_webhook_url_ok(self):
        params = {
            'ipsum_1': 'this is a test',
            'key2': 'value 456',
            'key3': 'xyzabc'
        }
        secrets = Secrets(
            _base_domain_name='ipsumlorem.com',
            _app_name='big-service',
            _environment='dev'
        )
        val = secrets.get_webhook_url(params=params)
        self.assertEqual(
            'https://big-service-dev.ipsumlorem.com/pingback-event?ipsum_1=this+is+a+test&key2=value+456&key3=xyzabc',
            val
        )
