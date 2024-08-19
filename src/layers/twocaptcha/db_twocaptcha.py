import typing
import uuid

from py_aws_core import decorators as aws_decorators, exceptions as aws_exceptions, entities
from py_aws_core.db_dynamo import ABCCommonAPI, DDBClient

from . import const, entities

__db_client = DDBClient()


def get_db_client():
    """
    Reuses db client across all modules for efficiency
    :return:
    """
    return __db_client


class TCDBAPI(ABCCommonAPI):
    CANCELLATION_ERROR_MAPS = []

    @classmethod
    def build_recaptcha_event_map(
        cls,
        captcha_id: str,
        params: typing.Dict[str, str],
    ):
        pk = sk = entities.RecaptchaEvent.create_key(captcha_id=captcha_id)
        return cls.get_batch_entity_create_map(
            expire_in_seconds=None,
            pk=pk,
            sk=sk,
            _type=entities.RecaptchaEvent.type(),
            CaptchaId=captcha_id,
            Code='',
            Params=params,
            Status=const.EventStatus.INIT.value,
        )

    class UpdateCaptchaEvent:
        """
            Updates Captcha Event statuses
        """

        @classmethod
        @aws_decorators.dynamodb_handler(client_err_map=aws_exceptions.ERR_CODE_MAP, cancellation_err_maps=[])
        def call(
            cls,
            db_client: DDBClient,
            captcha_id: str,
            status: const.EventStatus,
            code: str = None,
        ):
            pk = sk = entities.RecaptchaEvent.create_key(captcha_id=captcha_id)
            return db_client.update_item(
                key={
                    'PK': pk,
                    'SK': sk,
                },
                update_expression=f'SET Status = :sts, ModifiedAt = :mda, Code = :code',
                expression_attribute_values={
                    ':sts': {'S': status.value},
                    ':mda': {'S': TCDBAPI.iso_8601_now_timestamp()},
                    ':cde': {'S': code}
                },
            )
