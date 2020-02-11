import logging
from logging.config import dictConfig
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_mongoengine import MongoEngine
from config import Config
from flask_restplus import Api

logger = logging.getLogger(__name__)

api = Api()

app = Flask(__name__)
app.config.from_object(Config)

dictConfig(app.config.LOGGING)
logger.info("Logging configured",
            extra=dict(
                root_logger_level=logging.getLogger().getEffectiveLevel(),
                logger_level=logger.getEffectiveLevel()
            ))

db = MongoEngine()
db.init_app(app)
api.init_app(app)

toolbar = DebugToolbarExtension(app)

# We don't want to have circular dependencies so call application after we've called app.

from application import routes
