import os
from application.utils.logs import RequestIdFilter


class Config(object):
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or b"\xfd]\xa0\xb3\xf1\xbc\x02I\xc7\x8f_\x8d(EZi"
    )

    MONGODB_SETTINGS = {"db": "UTA_Enrollment"}

    MONGODB_SETTINGS = {
        "db": "UTA_Enrollment",
        "host": "mongodb://172.16.2.234/UTA_Enrollment",
    }

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {"request_id": {"()": RequestIdFilter,},},
        "formatters": {
            "json": {
                "format": "%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(filename)s %(lineno)s %(request_id)s %(message)s",
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            },
        },
        "handlers": {
            "console_message": {
                "class": "logging.StreamHandler",
                "level": "NOTSET",
                "formatter": "json",
                "filters": ["request_id"],
            },
        },
        "loggers": {
            "tests": {
                "handlers": ["console_message"],
                "propagate": False,
                "level": "DEBUG",
            },
            "flask": {
                "handlers": ["console_message"],
                "propagate": False,
                "level": os.environ.get("LOG_LEVEL", "WARNING"),
            },
            "werkzeug": {
                "handlers": ["console_message"],
                "propagate": False,
                "level": os.environ.get("LOG_LEVEL", "WARNING"),
            },
        },
        "root": {
            "handlers": ["console_message"],
            "level": os.environ.get("LOG_LEVEL", "WARNING"),
        },
    }
