# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import RoleMixin, UserMixin
from app import db, login
import time
from datetime import datetime, timedelta
import base64
import os


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
    )


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, index=True)
    name = db.Column(db.String(20), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), default=None)
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    clinets = db.relationship('Client', backref='user', lazy='dynamic')
    last_login_at = db.Column(db.DateTime())
    last_logout_at = db.Column(db.DateTime())
    # current_login_at = db.Column(db.DateTime())
    # last_login_ip = db.Column(db.String(100))
    # current_login_ip = db.Column(db.String(100))

    def get_client_count(self):
        count = Client.query.filter_by(user=self).count()
        return count


    def add_client(self, name):
        new_client = Client(name=name)
        new_client.user = self
        new_client.get_token()
        db.session.add(new_client)
        db.session.commit()
        return new_client.token


    def _update_last_login_time(self, date):
        self.last_login_at = date
        db.session.add(self)
        db.session.commit()

    def _update_last_logout_time(self, date):
        self.last_logout_at = date
        db.session.add(self)
        db.session.commit()        


    def to_dict(self):
        
        data = {
            'id' : self.id,
            'name' : self.name,
            'active' : self.active,
        }


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String(255))


class Data(db.Model):

    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    datestamp = db.Column(db.String)
    json = db.Column(db.String)
    parser_id = db.Column(db.Integer, db.ForeignKey('parsers.id'))
    

class Parser(db.Model):

    __tablename__ = 'parsers'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    data = db.relationship('Data', backref='parser', lazy='dynamic')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)


    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        client = Client.query.filter_by(token=token).first()
        if client is None or client.token_expiration < datetime.utcnow():
            return None
        return client


class Client(db.Model):

    __tablename__ = 'clients'

    id =  id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        client = Client.query.filter_by(token=token).first()
        if client is None or client.token_expiration < datetime.utcnow():
            return None
        return client



####################################################################################################
#   Классы форм
####################################################################################################

class LoginForm(FlaskForm):
    name = StringField('name', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    submit = SubmitField('Login')


class AddUserForm(FlaskForm):
    name = StringField('name', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    submit = SubmitField('Add')


class AddParserForm(FlaskForm):
    name = StringField('name', validators=[Required()])
    submit = SubmitField('Add')




