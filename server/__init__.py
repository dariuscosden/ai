from flask import Flask
from pathlib import Path
from server.database import db

import os


def create_app():

    # creates the app
    app = Flask(
        __name__,
        static_folder='../static/dist',
        template_folder='../static/templates')

    # configuration
    from instance.config import Configuration
    app.config.from_object(Configuration)

    # views
    with app.app_context():
        from server import views
        from server import ai

    # database
    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app
