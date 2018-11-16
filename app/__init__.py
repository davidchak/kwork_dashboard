# -*- coding: utf-8 -*-

from flask import Flask
import click
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

login_manager = LoginManager()


app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager.init_app(app)

from models import *
from routes import *

with app.app_context():
    db.create_all()


@app.cli.command()
def initdb():
    """Initialize the database."""
    click.echo('Init the db')


@app.cli.command()
@click.argument('name')
@click.argument('passwd')
def create_user(name, passwd):
    """Add new user account"""
    u = User(name=name)
    u.password_hash = generate_password_hash(passwd)
    db.session.add(u)
    db.session.commit()