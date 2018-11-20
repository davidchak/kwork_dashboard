# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Data(db.Model):

    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key = True)
    datestamp = db.Column(db.String)
    json = db.Column(db.String)
    parser_id = db.Column(db.Integer, db.ForeignKey('parsers.id'))
    

class Parser(db.Model):

    __tablename__ = 'parsers'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    data = db.relationship('Data', backref='parser', lazy='dynamic')


class LoginForm(FlaskForm):
    name = StringField('name', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    submit = SubmitField('Login')


class AddUserForm(FlaskForm):
    name = StringField('name', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    submit = SubmitField('Add')


class NewParserForm(FlaskForm):
    name = StringField('name', validators=[Required()])
    submit = SubmitField('Add')



