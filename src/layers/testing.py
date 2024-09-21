import json
import typing
from importlib.abc import Traversable
from importlib.resources import as_file, files

from py_aws_core.testing import BaseTestFixture


class CSTestFixture(BaseTestFixture):
    TEST_RESOURCE_PATH = files('tests._resources')

    TEST_API_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('api')
    TEST_DB_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('db')
    TEST_EVENT_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('events')

    TEST_VERIFICATION_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    TEST_RECAPTCHA_V2_TOKEN = '03AFcWeA5xt81XD7XGBySXzNt8X3lUR7Gc-5cmhirAZ1CEbn6tNGuNL-1AQ-nW_aYyebKBJRoC06H4c36PS_Z10aos7hD4TyHFcGAk_-v2BJ1iPwKZ7Aqh-QSoimCfoWQupkz9IKNuBrRlfXEnArur_6yKcuTMCAgvUg4YbHy_6nrnRhZyV5ovzNeTTrUVuMkhUP2JjeDepT0iNmD9lDzz_wXdiLEp3EY_TcJbdpnB_sbnMJU1bJIvgtrkmFLWpziVpseW7z7tDZO1q2U2t0IczZpOn4MkUbtCkYsNU6KZgDmY1PlgrT_LlgxitEoMo1jwDqqGYsJacN2CO4oeGhdPMKWoX6_F2QIwWzYTU05Bylhfem0bz8jJJsV8Q28xD9wbh7BCIi8gvMtozmUIbgk56LnijSdmiGhw1qu0exPA5_sx9jImA6By2zNj-0ULdfCoHx2xl_2A2XwpjxNolQhc8PrMOFK68UuBBFGZhUtRAc2iz47141MnNmXqj-3bwudWvnk8hK8FjWTAkPx-hY4yOJpwks0Rnfo-XVZK70ocUDeGDfIcZk9l25Rx94e9u3XbxAirHZFog9wem8KLLoc2AHs_GTfYgzwYdQ8dMy4IzcCXRUeffj73qb-D0BGioRDzaE5Uv4n2rZrqFnKvd1dxxek1j_k6fNG2Xo-IHlxC5VdYLlvQvDOok8jZl-XvYLwK8e6MxCdY1dwwzPTJ-LlDX9RiF99wkZVM4PiPOV5VnQ4WVWukKanvDOpROHKarYleKBekNskXmp-S8ek-rqr545D5F0UWnFVfdGelU8pgOg576S4YaN44wmfCJgGqgDE4S83VWMknvnLq5gnt_aHto4KFMKYnzO8jAK7jZQqIqJFSh3sJZMbGAsF34gNSO6Lq-VK-Ov6V_AH1HUeAXzpl5iOtzZrVkjHnlZzItFSFD0y8j7f3FFboTx0Qbs1kYneFCMC8gR_v6to9'
    TEST_SITEKEY = '6LeN_osaAAAAAL-8U6H1IWdcFCY9kDBS34OBYqL_'

    @classmethod
    def get_api_resource_json(cls, *descendants) -> typing.Dict:
        return cls.get_resource_json(*descendants, _path=cls.TEST_API_RESOURCE_PATH)

    @classmethod
    def get_event_resource_json(cls,  *descendants) -> typing.Dict:
        return cls.get_resource_json(*descendants, _path=cls.TEST_EVENT_RESOURCE_PATH)

    @classmethod
    def get_db_resource_json(cls, *descendants) -> typing.Dict:
        return cls.get_resource_json(*descendants, _path=cls.TEST_DB_RESOURCE_PATH)

    @classmethod
    def get_resource_json(cls, *descendants, _path: Traversable):
        source = _path.joinpath(*descendants)
        with as_file(source) as event_json:
            return json.loads(event_json.read_text())