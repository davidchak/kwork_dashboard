# -*- coding: utf-8 -*-

from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_moment import Moment
import cli


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
security = Security()
moment = Moment()



def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)
    moment.init_app(app)

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from app.dashboard import dashboard as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.api import api as api_bp
    app.register_blueprint(api_bp)

    from app.models import User, Role
    app.user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, app.user_datastore)

    with app.app_context():
        db.create_all()
  
    cli.register(app)

    return app

from app import models






