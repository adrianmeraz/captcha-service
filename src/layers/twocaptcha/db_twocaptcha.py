import typing

from py_aws_core import decorators as aws_decorators, exceptions as aws_exceptions, entities
from py_aws_core.db_dynamo import ABCCommonAPI, DDBClient

from src.layers import logs
from . import const, entities

logger = logs.logger
__db_client = DDBClient()


def get_db_client():
    """
    Reuses db client across all modules for efficiency
    :return:
    """
    return __db_client


class RecaptchaV2DB(ABCCommonAPI):
    EVENT_TYPE = const.EventCaptchaType.RECAPTCHA_V2

    @classmethod
    def recaptcha_v2_event_create_key(cls, captcha_id: str):
        return entities.CaptchaEvent.create_key(captcha_id=captcha_id, captcha_type=cls.EVENT_TYPE.RECAPTCHA_V2)


class CreateRecaptchaV2Event(RecaptchaV2DB):
    @classmethod
    def call(
        cls,
        db_client: DDBClient,
        captcha_id: str,
        params: typing.Dict[str, str],
    ) -> int:
        pk = sk = cls.recaptcha_v2_event_create_key(captcha_id=captcha_id)
        c_maps = [RecaptchaV2DB.get_batch_entity_create_map(
            expire_in_seconds=None,
            pk=pk,
            sk=sk,
            _type=entities.CaptchaEvent.type(),
            CaptchaId=captcha_id,
            CaptchaType=cls.EVENT_TYPE.value,
            Code='',
            Params=params,
            Status=const.EventStatus.INIT.value,
        )]
        count = db_client.write_maps_to_db(item_maps=c_maps)
        logger.info(f'{cls.__qualname__}#call, pk: {pk}, {count} record(s) written')
        return count


class UpdateCaptchaEvent(RecaptchaV2DB):
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
        pk = sk = cls.recaptcha_v2_event_create_key(captcha_id=captcha_id)
        r = db_client.update_item(
            key={
                'PK': pk,
                'SK': sk,
            },
            update_expression=f'SET Status = :sts, ModifiedAt = :mda, Code = :code',
            expression_attribute_values={
                ':sts': {'S': status.value},
                ':mda': {'S': RecaptchaV2DB.iso_8601_now_timestamp()},
                ':cde': {'S': code}
            },
        )
        logger.info(f'{cls.__qualname__}#call, pk: {pk}, record updated')
        return r
