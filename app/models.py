# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    @classmethod
    def set_password(password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def check_password(password):
        return check_password_hash(self.password_hash, password)



class LoginForm(FlaskForm):
    name = StringField('name', validators=[Required()])
    passwd = PasswordField('password', validators=[Required()])
    submit = SubmitField('Login')
