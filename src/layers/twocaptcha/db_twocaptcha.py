import typing

from py_aws_core import decorators as aws_decorators, exceptions as aws_exceptions
from py_aws_core.db_dynamo import ABCCommonAPI, DDBClient, UpdateItemResponse
from src.layers.twocaptcha import entities

from src.layers import const, logs, entities

logger = logs.logger
__db_client = DDBClient()


def get_db_client():
    """
    Reuses db client across all modules for efficiency
    :return:
    """
    return __db_client


class TwoCaptchaDB(ABCCommonAPI):
    pass


class CreateCaptchaEvent(TwoCaptchaDB):
    """
        Updates Captcha Events
    """

    class Response(UpdateItemResponse):

        @property
        def captcha_event(self) -> entities.CaptchaEvent:
            return entities.CaptchaEvent(self.attributes)

    @classmethod
    @aws_decorators.dynamodb_handler(client_err_map=aws_exceptions.ERR_CODE_MAP, cancellation_err_maps=[])
    def call(
        cls,
        db_client: DDBClient,
        captcha_id: str,
        status: const.EventStatus,
        code: str = None,
    ) -> Response:
        pk = sk = cls.recaptcha_v2_event_create_key(captcha_id=captcha_id)
        response = db_client.put_item(
            key=cls.serialize_types({
                'PK': pk,
                'SK': sk,
            }),
            update_expression=f'SET #est = :est, #mda = :mda, #cde = :cde',
            expression_attribute_names={
                '#est': 'EventStatus',
                '#mda': 'ModifiedAt',
                '#cde': 'Code',
            },
            expression_attribute_values=cls.serialize_types({
                ':est': status.value,
                ':mda': cls.iso_8601_now_timestamp(),
                ':cde': code,
            }),
            return_values='ALL_NEW'
        )
        logger.info(f'{cls.__qualname__}#call, pk: {pk}, record updated')
        return cls.Response(response)


class CreateTCWebhookEvent(TwoCaptchaDB):
    @classmethod
    @aws_decorators.dynamodb_handler(client_err_map=aws_exceptions.ERR_CODE_MAP, cancellation_err_maps=[])
    def call(cls, db_client: DDBClient, _id: str, code: str, rate: str):
        pk = sk = entities.TCWebhookEvent.create_key(_id=_id)
        _type = entities.TCWebhookEvent.type()
        item = cls.get_put_item_map(
            pk=pk,
            sk=sk,
            _type=_type,
            expire_in_seconds=None,
            Id=_id,
            Code=code,
            Rate=rate
        )
        response = db_client.put_item(
            Item=item,
        )
        logger.debug(f'{cls.__qualname__}.call# -> response: {response}')
        return response
