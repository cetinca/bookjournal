import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, session
from flask_mail import Mail
from pymongo import MongoClient

from routes import pages

load_dotenv()
mail = Mail()


def create_app():
    app = Flask(__name__)

    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=120)

    app.secret_key = os.environ.get("SECRET_KEY")
    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT")
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
    app.config['MAIL_PORT'] = os.environ.get("MAIL_PORT")
    app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
    app.config['MAIL_USE_SSL'] = os.environ.get("MAIL_USE_SSL")
    app.db = MongoClient(app.config["MONGODB_URI"]).get_default_database()
    app.mail = Mail(app)
    app.register_blueprint(pages)
    return app
