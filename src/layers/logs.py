import structlog

structlog.configure(
    processors=[
        structlog.processors.CallsiteParameterAdder(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.EventRenamer("message"),
        structlog.processors.JSONRenderer(),
    ]
)

__logger = structlog.get_logger(__name__)


def get_logger():
    return __logger
