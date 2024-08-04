import inspect
import logging
import sys
from typing import override

from loguru import logger


class InterceptHandler(logging.Handler):
    @override
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


LOCAL_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> | {extra}"


def config_logging(
    version: str, level: str | int = logging.INFO, is_local: bool = False
):
    logger.remove()
    if is_local:
        logger.add(sys.stderr, level=level, format=LOCAL_FORMAT)
    else:
        logger.add(sys.stderr, level=level, serialize=True, diagnose=False)
        logger.configure(extra={"version": version})

    logging.basicConfig(handlers=[InterceptHandler()], level=level, force=True)
