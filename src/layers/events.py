from py_aws_core.events import LambdaEvent


class HttpEvent(LambdaEvent):

    """
    TODO Maybe do some inspection of events here
    1. Linking person entities to em core travelers somehow.
    Could do this via local storage hashmaps
    Can expire the ids according to how long a checkmig session lasts
    """
    pass


class TwoCaptchaGetVerificationEvent(HttpEvent):
    pass
