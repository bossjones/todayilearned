# SOURCE: https://blog.bartab.fr/fastapi-logging-on-the-fly/
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

# pylint: disable=no-member


class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


class Course(db.Document):
    courseID = db.StringField(max_length=10, unique=True)
    title = db.StringField(max_length=100)
    description = db.StringField(max_length=255)
    credits = db.IntField()
    term = db.StringField(max_length=25)


class Enrollment(db.Document):
    user_id = db.IntField()
    courseID = db.StringField(max_length=10)


class LoggerPatch(BaseModel):
    name: str
    level: str


class LoggerModel(BaseModel):
    name: str
    level: Optional[int]
    children: Optional[List["LoggerModel"]] = None

LoggerModel.update_forward_refs()
