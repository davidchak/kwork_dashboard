# -*- coding: utf-8 -*-

from flask import g, Response, abort, jsonify, make_response
from app.models import Client, Parser, User
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from .errors import error_response
from datetime import datetime, timedelta


client_token_auth = HTTPTokenAuth()

parser_token_auth = HTTPTokenAuth()

users_basic_auth = HTTPBasicAuth()


@client_token_auth.verify_token
def verify_token(token):
    client = Client.query.filter_by(token=token).first()
    if client and client.active:

        if client.token_expiration < datetime.now():
            resp = make_response(jsonify({'error':'The key has expired!'}))
            resp.headers ['Content-Type'] = 'application/json'
            return abort(resp)
        else:
            client.update_last_login_time(datetime.now())
            return client 
    else: 
        return False


@client_token_auth.error_handler
def token_auth_error():
    return error_response(401)


@parser_token_auth.verify_token
def verify_token(token):

    parser = Parser.query.filter_by(token=token).first()
    if not parser:
        return None
    return parser


@users_basic_auth.verify_password
def verify_password(username, password):
    g.user = None
    user = User.query.filter_by(name=username).first()
    if user is not None and user.active and user.check_password(password):
        user._update_last_login_time(datetime.now())
        user._update_last_logout_time(datetime.now() + timedelta(seconds=1))
        g.user = user
        return True
    return False
