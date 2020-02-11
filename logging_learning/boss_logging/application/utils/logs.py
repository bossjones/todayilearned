from flask import request
import logging
import uuid
import flask


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if request:
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)


def generate_request_id(original_id=''):
    new_id = uuid.uuid4()

    if original_id:
        new_id = "{},{}".format(original_id, new_id)

    return new_id


def request_id():
    if getattr(flask.g, 'request_id', None):
        return flask.g.request_id

    headers = flask.request.headers
    original_request_id = headers.get("X-Request-Id")
    new_uuid = generate_request_id(original_request_id)
    flask.g.request_id = new_uuid

    return new_uuid


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id() if flask.has_request_context() else ''
        return True
