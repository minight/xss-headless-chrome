from flask import Flask
import logging
import os
from flask_sqlalchemy import SQLAlchemy

class ConfigClass(object):
    # Flask settings
    # DEBUG = True
    SECRET_KEY                      = 'fuckyouandyoursecretkey'
    SQLALCHEMY_DATABASE_URI         = 'postgresql+psycopg2://adminisbestusername:hunter2isbestpassword@db:5432/magicdatabase'
    SQLALCHEMY_ECHO                 = True
    FLAG = os.getenv("FLAG", "flag{noflaglol}")
    HOST = os.getenv("HOST", "http://localhost")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "memes_make_dreams")

db = SQLAlchemy()

def register_models(app):
    from .basic_bp import models

    with app.app_context():
        db.init_app(app)
        db.create_all()

        models.populate()

def register_blueprints(app):
    from .basic_bp import app as basic_bp
    app.register_blueprint(basic_bp)

def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__ + '.ConfigClass')

    register_models(app)
    register_blueprints(app)

    return app

