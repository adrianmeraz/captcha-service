from abc import ABC, abstractmethod

from . import tc_const


class ITwoCaptchaDatabase(ABC):
    @abstractmethod
    def create_webhook_event(
        self,
        captcha_id: str,
        code: str,
        rate: str
    ):
        pass

    def create_bad_captcha_report(
        self,
        captcha_id: str,
    ):
        self.create_captcha_report(captcha_id=captcha_id, status=tc_const.ReportStatus.BAD)

    def create_good_captcha_report(
        self,
        _id: str,
    ):
        self.create_captcha_report(captcha_id=_id, status=tc_const.ReportStatus.GOOD)

    @abstractmethod
    def create_captcha_report(
        self,
        captcha_id: str,
        status: tc_const.ReportStatus,
    ):
        pass
