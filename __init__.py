import os

from flask import (
    Flask, url_for, render_template, redirect
)
from datetime import datetime
from pprint import pprint


def create_app():
    app = Flask(__name__)
    app.secret_key = 'h@h@HAhahaVERYs3cr3tKeY'

    from tasktracker import db
    from tasktracker import auth, tasks

    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)

    @app.route('/')
    def index():
        return redirect(url_for('tasks.open_tasks'))

    @app.template_filter('local_date')
    def local_date(date_string):
        if date_string:
            date_object = datetime.strptime(date_string, '%Y-%m-%d')
            result = datetime.strftime(date_object, '%d.%m.%Y')
        else:
            result = ''
        return result

    return app
