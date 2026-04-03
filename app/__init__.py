from .extensions import db
from flask import Flask, Blueprint
import os
from dotenv import load_dotenv
from app.extensions import login_manager, cache, limiter
from app.routes import unprotected, protected


load_dotenv()




def create_flask_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("APP_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    #maximum size of image set to 16mb
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000


    #initialise db extension
    db.init_app(app)
    #initialise login manager extension
    login_manager.init_app(app)
    login_manager.login_view = "unprotected.login"
    login_manager.login_message_category = "info"
    #initialise cache extension
    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})
    #initialise Limiter
    limiter.init_app(app)

    # register Blueprint
    app.register_blueprint(unprotected)
    app.register_blueprint(protected)
    app.register_blueprint(ajax_rule)
    # print(app.url_map)


    return app


