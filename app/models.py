# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import RoleMixin, UserMixin, current_user
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
    clinets = db.relationship('Client', backref='user', lazy='dynamic')
    last_login_at = db.Column(db.DateTime())
    last_logout_at = db.Column(db.DateTime())
    parent_id = db.Column(db.Integer)

    def get_client_count(self):
        count = Client.query.filter_by(user=self).count()
        return count
    
    def activ_deactiv_user(self):
        if self.active == True:
            self.active = False
        elif self.active == False:
            self.active = True 

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
            'role' : self.roles[0].name,
            'last_login_at': self.last_login_at,
            'last_logout_at': self.last_logout_at,
        }
        return data


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model, RoleMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String(255))
    users = db.relationship('User', secondary=roles_users, backref=db.backref('roles', lazy='dynamic'))

class Data(db.Model):

    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    datestamp = db.Column(db.DateTime)
    json = db.Column(db.String)
    parser_id = db.Column(db.Integer, db.ForeignKey('parsers.id'))
    

class Parser(db.Model):

    __tablename__ = 'parsers'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    data = db.relationship('Data', backref='parser', lazy='dynamic')
    token = db.Column(db.String(32), index=True, unique=True)
    parent_id = db.Column(db.Integer)

    def get_token(self, expires_in=432000):
        now = datetime.utcnow()
        if self.token:
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        db.session.add(self)
        return self.token


    def to_dict(self, parent_id):
        if self.parent_id == parent_id or parent_id == 1:
            parser_data = []
            for i in self.data:
                parser_data.append({
                    'id': i.id,
                    'datestamp': i.datestamp,
                    'json': i.json
                })
            data = {
                'id': self.id,
                'name': self.name,
                'token': self.token,
                'data': parser_data
            } 
        else:
            data = None
        
        return data

    def set_data(self, datestamp, json):
        data = Data()
        data.datestamp = datestamp
        data.parser = self
        data.json = json
        db.session.add(data)
        db.session.commit()
        

class Client(db.Model):

    __tablename__ = 'clients'

    id =  id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime())
    parent_id = db.Column(db.Integer)


    def get_token(self, expires_in=10):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(days=expires_in)
        db.session.add(self)
        return self.token
    
    def update_token_expiration(self, num):
        now = datetime.utcnow()
        self.token_expiration = now + timedelta(days=num)

    def update_last_login_time(self, date):
        self.last_login_at = date
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'active': self.active,
            'token': self.token,
            'token_expiration': self.token_expiration
        }
        return data

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def activ_deactiv_client(self):
        if self.active == True:
            self.active = False
        elif self.active == False:
            self.active = True


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




