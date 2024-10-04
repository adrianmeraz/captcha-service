import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.EventRenamer("msg"),
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.get_logger(__name__)
