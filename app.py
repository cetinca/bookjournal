import os
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import Flask

from routes import pages

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY")
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    app.db = MongoClient(app.config["MONGODB_URI"]).get_default_database()
    app.register_blueprint(pages)
    return app