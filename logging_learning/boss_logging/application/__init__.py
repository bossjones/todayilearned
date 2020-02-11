from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_mongoengine import MongoEngine
from config import Config
from flask_restplus import Api

api = Api()

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)
api.init_app(app)

toolbar = DebugToolbarExtension(app)

# We don't want to have circular dependencies so call application after we've called app.

from application import routes
