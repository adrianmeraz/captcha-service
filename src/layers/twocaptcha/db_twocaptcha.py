from py_aws_core import decorators as aws_decorators
from py_aws_core.db_dynamo import ABCCommonAPI, DDBClient, DDBItemResponse

from src.layers import logs
from src.layers.twocaptcha import const, entities, exceptions

logger = logs.get_logger()
__db_client = DDBClient()


def get_db_client():
    """
    Reuses db client across all modules for efficiency
    :return:
    """
    return __db_client


class TwoCaptchaDB(ABCCommonAPI):
    pass


class CreateTCWebhookEvent(TwoCaptchaDB):
    ERR_CODE_MAP = {
        'ConditionalCheckFailedException': exceptions.DuplicateTCWebhookEvent
    }

    class Response(DDBItemResponse):
        pass

    @classmethod
    @aws_decorators.dynamodb_handler(client_err_map=ERR_CODE_MAP, cancellation_err_maps=[])
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
        logger.debug(response)
        return cls.Response(response)


class CreateTCCaptchaReport(TwoCaptchaDB):
    ERR_CODE_MAP = {
        'ConditionalCheckFailedException': exceptions.DuplicateTCCaptchaReport
    }

    class Response(DDBItemResponse):
        pass

    @classmethod
    @aws_decorators.dynamodb_handler(client_err_map=ERR_CODE_MAP, cancellation_err_maps=[])
    def call(cls, db_client: DDBClient, _id: str, status: const.ReportStatus):
        pk = sk = entities.TCCaptchaReport.create_key(_id=_id)
        _type = entities.TCCaptchaReport.type()
        item = cls.get_put_item_map(
            pk=pk,
            sk=sk,
            _type=_type,
            expire_in_seconds=None,
            Id=_id,
            Status=status.value,
        )
        response = db_client.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(PK)',
        )
        logger.debug(response)
        return cls.Response(response)
