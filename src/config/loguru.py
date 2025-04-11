import sys

from src.middleware.logger_middleware import REQUEST_UUID


def add_request_uuid(record):
    record["extra"]["request_uuid"] = REQUEST_UUID.get()


def logger_config():
    return {
        "handlers": [
            {
                "sink": sys.stdout,
                "format": "<green>{time}</green> | <level>{level}</level> | <cyan>{name}<white>:</white>{function}<white>:</white>{line}</cyan> | <magenta>{extra[request_uuid]}</magenta> | <white>{message}</white>",  # noqa
                "serialize": False,
                "level": "INFO",
                "filter": lambda record: record["level"].name == "INFO",
            },
            {
                "sink": sys.stdout,
                "format": "<green>{time}</green> | <red>{level}</red> | <cyan>{name}<white>:</white>{function}<white>:</white>{line}</cyan> | <magenta>{extra[request_uuid]}</magenta> | <red>{message}</red>",  # noqa
                "serialize": False,
                "level": "ERROR",
                "filter": lambda record: record["level"].name == "ERROR",
            },
            {
                "sink": sys.stdout,
                "format": "<green>{time}</green> | <yellow>{level}</yellow> | <cyan>{name}<white>:</white>{function}<white>:</white>{line}</cyan> | <magenta>{extra[request_uuid]}</magenta> | <yellow>{message}</yellow>",  # noqa
                "serialize": False,
                "level": "WARNING",
                "filter": lambda record: record["level"].name == "WARNING",
            },
            {
                "sink": sys.stdout,
                "format": "<green>{time}</green> | <blue>{level}</blue> | <cyan>{name}<white>:</white>{function}<white>:</white>{line}</cyan> | <magenta>{extra[request_uuid]}</magenta> | <blue>{message}</blue>",  # noqa
                "serialize": False,
                "level": "DEBUG",
                "filter": lambda record: record["level"].name == "DEBUG",
            },
        ],
        "patcher": add_request_uuid,
    }
