import os


class Config(object):
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or b"\xfd]\xa0\xb3\xf1\xbc\x02I\xc7\x8f_\x8d(EZi"
    )

    MONGODB_SETTINGS = {"db": "UTA_Enrollment"}

    MONGODB_SETTINGS = {
        "db": "UTA_Enrollment",
        "host": "mongodb://172.16.2.234/UTA_Enrollment",
    }
