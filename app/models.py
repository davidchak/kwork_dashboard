# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import RoleMixin, UserMixin
from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
    )


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), default=None)
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

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



