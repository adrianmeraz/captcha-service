from py_aws_core import decorators as aws_decorators, exceptions as aws_exceptions
from py_aws_core.db_dynamo import ABCCommonAPI, DDBClient, UpdateItemResponse

from src.layers import const, logs
from src.layers.twocaptcha import entities

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
    @classmethod
    @aws_decorators.dynamodb_handler(client_err_map=aws_exceptions.ERR_CODE_MAP, cancellation_err_maps=[])
    def call(
        cls,
        db_client: DDBClient,
        _id: str,
        code: str,
        rate: str
    ):
        pk = sk = entities.TCWebhookEvent.create_key(_id=_id)
        item = cls.get_put_item_map(
            pk=pk,
            sk=sk,
            _type=entities.TCWebhookEvent.type(),
            expire_in_seconds=None,
            Code=code,
            Rate=rate
        )
        response = db_client.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(pk)',
        )
        logger.info(f'{cls.__qualname__}#call -> response: {response}')
        return response


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
            ConditionExpression='attribute_not_exists(PK)',
        )
        logger.debug(f'{cls.__qualname__}.call# -> response: {response}')
        return response
