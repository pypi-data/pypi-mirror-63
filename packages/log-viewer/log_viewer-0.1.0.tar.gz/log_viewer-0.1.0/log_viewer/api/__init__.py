import os

from flask import Flask

from log_viewer.api.v0.logs import logs_api_v1


app = Flask(__name__)
app.register_blueprint(logs_api_v1)
app.secret_key = os.urandom(24)
