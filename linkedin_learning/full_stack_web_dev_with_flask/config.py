import os


class Config(object):
    SECRET_KY = os.environ.get("SECRET_KEY") or "secret_string"

    MONGODB_SETTINGS = {"db": "UTA_Enrollment"}

    MONGODB_SETTINGS = {
        "db": "UTA_Enrollment",
        "host": "mongodb://172.16.2.234/UTA_Enrollment",
    }
