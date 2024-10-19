from botocore.client import BaseClient
from py_aws_core import decorators as aws_decorators
from py_aws_core.dynamodb_api import DynamoDBAPI
from py_aws_core.dynamodb_entities import ItemResponse

from src.layers.twocaptcha import tc_const, entities, exceptions


class TCDynamoDBAPI(DynamoDBAPI):
    pass


class CreateTCWebhookEvent(TCDynamoDBAPI):
    ERR_CODE_MAP = {
        'ConditionalCheckFailedException': exceptions.DuplicateTCWebhookEvent
    }

    class Response(ItemResponse):
        pass

    @classmethod
    @aws_decorators.dynamodb_handler(client_err_map=ERR_CODE_MAP, cancellation_err_maps=[])
    def call(cls, boto_client: BaseClient, table_name: str, captcha_id: str, code: str, rate: str):
        pk = sk = entities.TCWebhookEvent.create_key(_id=captcha_id)
        _type = entities.TCWebhookEvent.type()
        item = cls.get_put_item_map(
            pk=pk,
            sk=sk,
            _type=_type,
            expire_in_seconds=None,
            Id=captcha_id,
            Code=code,
            Rate=rate
        )
        response = boto_client.put_item(
            TableName=table_name,
            Item=item,
            ConditionExpression='attribute_not_exists(PK)',
        )
        return cls.Response(response)


class CreateTCCaptchaReport(TCDynamoDBAPI):
    ERR_CODE_MAP = {
        'ConditionalCheckFailedException': exceptions.DuplicateTCCaptchaReport
    }

    class Response(ItemResponse):
        pass

    @classmethod
    @aws_decorators.dynamodb_handler(client_err_map=ERR_CODE_MAP, cancellation_err_maps=[])
    def call(cls, boto_client: BaseClient, table_name: str, captcha_id: str, status: tc_const.ReportStatus):
        pk = sk = entities.TCCaptchaReport.create_key(_id=captcha_id)
        _type = entities.TCCaptchaReport.type()
        item = cls.get_put_item_map(
            pk=pk,
            sk=sk,
            _type=_type,
            expire_in_seconds=None,
            Id=captcha_id,
            Status=status.value,
        )
        response = boto_client.put_item(
            TableName=table_name,
            Item=item,
            ConditionExpression='attribute_not_exists(PK)',
        )
        return cls.Response(response)
