from flask import (
    Flask, url_for, render_template,
)


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "hello"

    return app
