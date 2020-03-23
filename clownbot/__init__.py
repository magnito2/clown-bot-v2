# app/__init__.py

import os

from flask import Flask

from .config import app_config


def create_app(config_name):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from .database.db import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
