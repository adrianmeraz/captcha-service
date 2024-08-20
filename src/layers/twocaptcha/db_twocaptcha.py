import typing

from py_aws_core import decorators as aws_decorators, db_dynamo, exceptions as aws_exceptions, entities
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

# class BaseRecaptchaV2EventDB(RecaptchaV2DB):
#


class CreateRecaptchaV2Event(RecaptchaV2DB):
    @classmethod
    def call(
        cls,
        db_client: DDBClient,
        captcha_id: str,
        webhook_data: typing.Dict[str, str],
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
            EventStatus=const.EventStatus.INIT.value,
            WebhookData=webhook_data,
            WebhookUrl=webhook_url,
            WebhookStatus=const.WebhookStatus.INIT.value
        )]
        count = db_client.write_maps_to_db(item_maps=c_maps)
        logger.info(f'{cls.__qualname__}#call, pk: {pk}, {count} record(s) written')
        return count


class UpdateCaptchaEvent(RecaptchaV2DB):
    """
        Updates Captcha Events
    """
    class Response(db_dynamo.QueryResponse):
        @property
        def captcha_event(self) -> entities.CaptchaEvent:
            return [entities.CaptchaEvent(s) for s in self.get_by_type(entities.CaptchaEvent.TYPE)][0]

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
        response = db_client.update_item(
            key={
                'PK': {'S': pk},
                'SK': {'S': sk},
            },
            update_expression=f'SET #est = :est, #mda = :mda, #cde = :cde',
            expression_attribute_names={
                '#est': 'EventStatus',
                '#mda': 'ModifiedAt',
                '#cde': 'Code',
            },
            expression_attribute_values={
                ':est': {'S': status.value},
                ':mda': {'S': RecaptchaV2DB.iso_8601_now_timestamp()},
                ':cde': {'S': code}
            },
            return_values='ALL_NEW'
        )
        logger.info(f'{cls.__qualname__}#call, pk: {pk}, record updated')
        return cls.Response(response)


class UpdateCaptchaEventWebookStatus(RecaptchaV2DB):
    """
        Updates Captcha Event Webhook Status
    """
    # class Response(db_dynamo.QueryResponse):
    #     @property
    #     def captcha_event(self) -> entities.CaptchaEvent:
    #         return [entities.CaptchaEvent(s) for s in self.get_by_type(entities.CaptchaEvent.TYPE)][0]

    class UpdateResponse:
        def __init__(self, data: typing.Dict):
            self.attributes = data['Attributes']

        @property
        def captcha_event(self) -> entities.CaptchaEvent:
            return entities.CaptchaEvent(self.attributes)

    @classmethod
    @aws_decorators.dynamodb_handler(client_err_map=aws_exceptions.ERR_CODE_MAP, cancellation_err_maps=[])
    def call(
        cls,
        db_client: DDBClient,
        captcha_id: str,
        webhook_status: const.WebhookStatus,
    ):
        pk = sk = cls.recaptcha_v2_event_create_key(captcha_id=captcha_id)
        response = db_client.update_item(
            key={
                'PK': {'S': pk},
                'SK': {'S': sk},
            },
            update_expression=f'SET #wst = :wst, #mda = :mda',
            expression_attribute_names={
                '#wst': 'WebhookStatus',
                '#mda': 'ModifiedAt',
            },
            expression_attribute_values={
                ':wst': {'S': webhook_status.value},
                ':mda': {'S': RecaptchaV2DB.iso_8601_now_timestamp()},
            },
            return_values='ALL_NEW'
        )
        logger.info(f'{cls.__qualname__}#call, pk: {pk}, record updated')
        return cls.UpdateResponse(response)
