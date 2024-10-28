from importlib.resources import files

from py_aws_core.boto_clients import SSMClient, DynamoTable
from py_aws_core.testing import BaseTestFixture

from src.layers.entities import CaptchaEvent
from src.layers.captcha_service import CaptchaService
from src.layers.db_service import DatabaseService
from src.layers.secrets import Secrets


class CSTestFixture(BaseTestFixture):
    TEST_RESOURCE_PATH = files('tests._resources')

    TEST_API_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('api')
    TEST_DB_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('db')
    TEST_EVENT_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('events')

    TEST_TWOCAPTCHA_VERIFICATION_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    TEST_RECAPTCHA_V2_TOKEN = '03AFcWeA5xt81XD7XGBySXzNt8X3lUR7Gc-5cmhirAZ1CEbn6tNGuNL-1AQ-nW_aYyebKBJRoC06H4c36PS_Z10aos7hD4TyHFcGAk_-v2BJ1iPwKZ7Aqh-QSoimCfoWQupkz9IKNuBrRlfXEnArur_6yKcuTMCAgvUg4YbHy_6nrnRhZyV5ovzNeTTrUVuMkhUP2JjeDepT0iNmD9lDzz_wXdiLEp3EY_TcJbdpnB_sbnMJU1bJIvgtrkmFLWpziVpseW7z7tDZO1q2U2t0IczZpOn4MkUbtCkYsNU6KZgDmY1PlgrT_LlgxitEoMo1jwDqqGYsJacN2CO4oeGhdPMKWoX6_F2QIwWzYTU05Bylhfem0bz8jJJsV8Q28xD9wbh7BCIi8gvMtozmUIbgk56LnijSdmiGhw1qu0exPA5_sx9jImA6By2zNj-0ULdfCoHx2xl_2A2XwpjxNolQhc8PrMOFK68UuBBFGZhUtRAc2iz47141MnNmXqj-3bwudWvnk8hK8FjWTAkPx-hY4yOJpwks0Rnfo-XVZK70ocUDeGDfIcZk9l25Rx94e9u3XbxAirHZFog9wem8KLLoc2AHs_GTfYgzwYdQ8dMy4IzcCXRUeffj73qb-D0BGioRDzaE5Uv4n2rZrqFnKvd1dxxek1j_k6fNG2Xo-IHlxC5VdYLlvQvDOok8jZl-XvYLwK8e6MxCdY1dwwzPTJ-LlDX9RiF99wkZVM4PiPOV5VnQ4WVWukKanvDOpROHKarYleKBekNskXmp-S8ek-rqr545D5F0UWnFVfdGelU8pgOg576S4YaN44wmfCJgGqgDE4S83VWMknvnLq5gnt_aHto4KFMKYnzO8jAK7jZQqIqJFSh3sJZMbGAsF34gNSO6Lq-VK-Ov6V_AH1HUeAXzpl5iOtzZrVkjHnlZzItFSFD0y8j7f3FFboTx0Qbs1kYneFCMC8gR_v6to9'
    TEST_SITEKEY = '6LeN_osaAAAAAL-8U6H1IWdcFCY9kDBS34OBYqL_'

    @classmethod
    def get_api_resource_json(cls, *descendants) -> dict:
        return cls.get_resource_json(*descendants, path=cls.TEST_API_RESOURCE_PATH)

    @classmethod
    def get_event_resource_json(cls,  *descendants) -> dict:
        return cls.get_resource_json(*descendants, path=cls.TEST_EVENT_RESOURCE_PATH)

    @classmethod
    def get_db_resource_json(cls, *descendants) -> dict:
        return cls.get_resource_json(*descendants, path=cls.TEST_DB_RESOURCE_PATH)

    @classmethod
    def get_mocked_captcha_event(cls):
        return CaptchaEvent(
            data={
                "CaptchaId": "77786017049",
                "Code": "",
                "ExpiresAt": "",
                "ProxyUrl": None,
                "CaptchaStatus": "INIT",
                "WebhookMaxAttempts": "3",
                "CaptchaType": "RECAPTCHA_V2",
                "PageUrl": "https://apps.migracioncolombia.gov.co/pre-registro/es/DatosBiograficos",
                "ModifiedAt": "2024-10-27T04:13:42+00:00",
                "Type": "CAPTCHA_EVENT",
                "WebhookStatus": "INIT",
                "WebhookData": {
                    "session_id": "52829e6ef9804ef39b221c7d74859a0a"
                },
                "SiteKey": "6LeN_osaAAAAAL-8U6H1IWdcFCY9kDBS34OBYqL_",
                "WebhookUrl": "https://co-checkmig-dev.mechnetworks.com/bio-post-captcha-token-webhook",
                "CaptchaMaxAttempts": "3",
                "SK": "CAPTCHA_EVENT#RECAPTCHA_V2#77786017049",
                "WebhookAttempts": "0",
                "PK": "CAPTCHA_EVENT#RECAPTCHA_V2#77786017049",
                "CaptchaAttempts": "0",
                "CreatedAt": "2024-10-27T04:13:42+00:00"
            }
        )

    @classmethod
    def get_mocked_captcha_service(cls, dynamo_table: DynamoTable):
        secrets = cls.get_mocked_secrets()
        db_service = DatabaseService(dynamo_table=dynamo_table)
        return CaptchaService(db_service=db_service, secrets=secrets)

    @classmethod
    def get_mocked_secrets(cls):
        ssm_client = SSMClient()
        return Secrets(
            ssm_client=ssm_client,
            app_name='big-service',
            base_domain_name='ipsumlorem.com',
            captcha_password='test-password-1',
            dynamo_db_table_name='TEST_TABLE',
            environment='dev',
            twocaptcha_pingback_token=cls.TEST_TWOCAPTCHA_VERIFICATION_TOKEN
        )

