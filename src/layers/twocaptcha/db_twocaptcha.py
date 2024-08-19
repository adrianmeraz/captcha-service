import typing

from py_aws_core import decorators as aws_decorators, exceptions as aws_exceptions, entities
from py_aws_core.db_dynamo import ABCCommonAPI, DDBClient

from src.layers import const, logs, entities

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
    def recaptcha_v2_event_create_key(cls, captcha_id: str) -> str:
        return entities.CaptchaEvent.create_key(captcha_id=captcha_id, captcha_type=cls.EVENT_TYPE.RECAPTCHA_V2)


class CreateRecaptchaV2Event(RecaptchaV2DB):
    @classmethod
    def call(
        cls,
        db_client: DDBClient,
        captcha_id: str,
        webhook_params: typing.Dict[str, str],
        webhook_url: str,
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
            Status=const.EventStatus.INIT.value,
            WebhookParams=webhook_params,
            WebhookUrl=webhook_url,
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
                'PK': {'S': pk},
                'SK': {'S': sk},
            },
            update_expression=f'SET #sts = :sts, #mda = :mda, #cde = :cde',
            expression_attribute_names={
                '#sts': 'Status',
                '#mda': 'ModifiedAt',
                '#cde': 'Code',
            },
            expression_attribute_values={
                ':sts': {'S': status.value},
                ':mda': {'S': RecaptchaV2DB.iso_8601_now_timestamp()},
                ':cde': {'S': code}
            },
            return_values='ALL_NEW'
        )
        logger.info(f'{cls.__qualname__}#call, pk: {pk}, record updated')
        return r
