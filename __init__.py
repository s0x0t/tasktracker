import os

from flask import (
    Flask, url_for, render_template,
)
from pprint import pprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from tasktracker import db
    from tasktracker import auth, tasks

    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
