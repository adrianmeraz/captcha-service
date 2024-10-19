from py_aws_core.boto_clients import SSMClientFactory

from src.layers.secrets import Secrets
from src.layers.testing import CSTestFixture


class SecretsTests(CSTestFixture):
    def test_get_webhook_url_ok(self):
        params = {
            'ipsum_1': 'this is a test',
            'key2': 'value 456',
            'key3': 'xyzabc'
        }
        boto_client = SSMClientFactory.new_client()
        secrets = Secrets(
            app_name='big-service',
            boto_client=boto_client,
            base_domain_name='ipsumlorem.com',
            captcha_password='test-password-1',
            dynamo_db_table_name='TEST_TABLE',
            environment='dev',
            twocaptcha_pingback_token='abcxyz'
        )
        val = secrets.get_webhook_url(params=params)
        self.assertEqual(
            'https://big-service-dev.ipsumlorem.com/pingback-event?ipsum_1=this+is+a+test&key2=value+456&key3=xyzabc',
            val
        )
