import typing

from py_aws_core import decorators as aws_decorators, exceptions as aws_exceptions, entities
from py_aws_core.db_dynamo import ABCCommonAPI, DDBClient, UpdateItemResponse

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


class GetOrCreateRecaptchaV2Event(RecaptchaV2DB):
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
        page_url: str,
        site_key: str,
        webhook_data: typing.Dict[str, str],
        webhook_url: str,
        proxy_url: str = '',
    ):
        pk = sk = cls.recaptcha_v2_event_create_key(captcha_id=captcha_id)
        _type = entities.CaptchaEvent.type()
        now = cls.iso_8601_now_timestamp()
        update_fields = [
            cls.UpdateField(expression_attr='ea', set_once=True),
            cls.UpdateField(expression_attr='ca', set_once=True),
            cls.UpdateField(expression_attr='ma'),
            cls.UpdateField(expression_attr='ty', set_once=True),
            cls.UpdateField(expression_attr='ci', set_once=True),
            cls.UpdateField(expression_attr='cp', set_once=True),
            cls.UpdateField(expression_attr='cm', set_once=True),
            cls.UpdateField(expression_attr='cy', set_once=True),
            cls.UpdateField(expression_attr='co', set_once=True),
            cls.UpdateField(expression_attr='cs', set_once=True),
            cls.UpdateField(expression_attr='pa', set_once=True),
            cls.UpdateField(expression_attr='pr', set_once=True),
            cls.UpdateField(expression_attr='si', set_once=True),
            cls.UpdateField(expression_attr='wd', set_once=True),
            cls.UpdateField(expression_attr='wu', set_once=True),
            cls.UpdateField(expression_attr='ws', set_once=True),
            cls.UpdateField(expression_attr='wa', set_once=True),
            cls.UpdateField(expression_attr='wm', set_once=True),
        ]
        response = db_client.update_item(
            Key=cls.serialize_types({
                'PK': pk,
                'SK': sk,
            }),
            UpdateExpression=cls.build_update_expression(update_fields),
            ExpressionAttributeNames={
                '#ea': 'ExpiresAt',
                '#ca': 'CreatedAt',
                '#ma': 'ModifiedAt',
                '#ty': 'Type',
                "#ci": 'CaptchaId',
                "#cp": 'CaptchaAttempts',
                "#cm": 'CaptchaMaxAttempts',
                "#cy": 'CaptchaType',
                "#co": 'Code',
                "#cs": 'CaptchaStatus',
                "#pa": 'PageUrl',
                "#pr": 'ProxyUrl',
                "#si": 'SiteKey',
                "#wd": 'WebhookData',
                "#wu": 'WebhookUrl',
                "#ws": 'WebhookStatus',
                "#wa": 'WebhookAttempts',
                "#wm": 'WebhookMaxAttempts',
            },
            ExpressionAttributeValues=cls.serialize_types({
                ':ea': cls.calc_expire_at_timestamp(expire_in_seconds=None),
                ':ca': now,
                ':ma': now,
                ':ty': _type,
                ':ci': captcha_id,
                ':cp': 0,
                ':cm': const.DEFAULT_WEBHOOK_MAX_ATTEMPTS,
                ':cy': cls.EVENT_TYPE.value,
                ':co': '',
                ':cs': const.CaptchaStatus.INIT.value,
                ':pa': page_url,
                ':pr': proxy_url,
                ':si': site_key,
                ':wd': webhook_data,
                ':wu': webhook_url,
                ':ws': const.WebhookStatus.INIT.value,
                ':wa': 0,
                ':wm': const.DEFAULT_WEBHOOK_MAX_ATTEMPTS
            }),
            ReturnValues='ALL_NEW'
        )

        logger.debug(f'{cls.__qualname__}.call# -> response: {response}')
        return cls.Response(response)


class CreateRecaptchaV2Event(RecaptchaV2DB):
    @classmethod
    def call(
        cls,
        db_client: DDBClient,
        captcha_id: str,
        page_url: str,
        proxy_url: str,
        site_key: str,
        webhook_data: typing.Dict[str, str],
        webhook_url: str,
    ) -> int:
        pk = sk = cls.recaptcha_v2_event_create_key(captcha_id=captcha_id)
        c_maps = [cls.get_batch_entity_create_map(
            expire_in_seconds=None,
            pk=pk,
            sk=sk,
            _type=entities.CaptchaEvent.type(),
            CaptchaId=captcha_id,
            CaptchaAttempts=0,
            CaptchaMaxAttempts=const.DEFAULT_CAPTCHA_MAX_ATTEMPTS,
            CaptchaType=cls.EVENT_TYPE.value,
            Code='',
            CaptchaStatus=const.CaptchaStatus.INIT.value,
            PageUrl=page_url,
            ProxyUrl=proxy_url,
            SiteKey=site_key,
            WebhookData=webhook_data,
            WebhookUrl=webhook_url,
            WebhookStatus=const.WebhookStatus.INIT.value,
            WebhookAttempts=0,
            WebhookMaxAttempts=const.DEFAULT_WEBHOOK_MAX_ATTEMPTS
        )]
        count = db_client.write_maps_to_db(item_maps=c_maps)
        logger.info(f'{cls.__qualname__}#call, pk: {pk}, {count} record(s) written')
        return count


class UpdateCaptchaEventCode(RecaptchaV2DB):
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
        status: const.CaptchaStatus,
        code: str,
    ) -> Response:
        pk = sk = cls.recaptcha_v2_event_create_key(captcha_id=captcha_id)
        response = db_client.update_item(
            Key=cls.serialize_types({
                'PK': pk,
                'SK': sk,
            }),
            UpdateExpression=f'SET #est = :est, #mda = :mda, #cde = :cde',
            ExpressionAttributeNames={
                '#est': 'CaptchaStatus',
                '#mda': 'ModifiedAt',
                '#cde': 'Code',
            },
            ExpressionAttributeValues=cls.serialize_types({
                ':est': status.value,
                ':mda': cls.iso_8601_now_timestamp(),
                ':cde': code,
            }),
            ReturnValues='ALL_NEW'
        )
        logger.info(f'{cls.__qualname__}#call, pk: {pk}, record updated')
        return cls.Response(response)


class UpdateCaptchaEventOnSolveAttempt(RecaptchaV2DB):
    """
        Updates CaptchaAttempts counter and Captcha Status
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
    ) -> Response:
        pk = sk = cls.recaptcha_v2_event_create_key(captcha_id=captcha_id)
        response = db_client.update_item(
            Key=cls.serialize_types({
                'PK': pk,
                'SK': sk,
            }),
            UpdateExpression=f'SET #cs = :cs, #ma = :ma ADD #cp :inc',
            ExpressionAttributeNames={
                '#ma': 'ModifiedAt',
                '#cs': 'CaptchaStatus',
                '#cp': 'CaptchaAttempts',
            },
            ExpressionAttributeValues=cls.serialize_types({
                ':ma': cls.iso_8601_now_timestamp(),
                ':cs': const.CaptchaStatus.CAPTCHA_SOLVING,
                ':inc': 1
            }),
            ReturnValues='ALL_NEW'
        )
        logger.info(f'{cls.__qualname__}#call, pk: {pk}, record updated')
        return cls.Response(response)


class UpdateCaptchaEventWebhook(RecaptchaV2DB):
    """
        Updates Captcha Event Webhook Status
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
        webhook_status: const.WebhookStatus,
    ) -> Response:
        pk = sk = cls.recaptcha_v2_event_create_key(captcha_id=captcha_id)
        response = db_client.update_item(
            Key=cls.serialize_types({
                'PK': pk,
                'SK': sk,
            }),
            UpdateExpression=f'SET #wst = :ws, #ma = :ma ADD #wa :inc',
            ExpressionAttributeNames={
                '#wst': 'WebhookStatus',
                '#wa': 'WebhookAttempts',
                '#ma': 'ModifiedAt',
            },
            ExpressionAttributeValues=cls.serialize_types({
                ':ws': webhook_status.value,
                ':ma': cls.iso_8601_now_timestamp(),
                ':inc': 1
            }),
            ReturnValues='ALL_NEW'
        )
        logger.info(f'{cls.__qualname__}#call, pk: {pk}, record updated')
        return cls.Response(response)