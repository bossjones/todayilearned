from flask import Flask

app = Flask(__name__)

# We don't want to have circular dependencies so call application after we've called app.

from application import routes
