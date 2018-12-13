# -*- coding: utf-8 -*-

from flask import g, Response, abort, jsonify, make_response
from app.models import Client, Parser
from flask_httpauth import HTTPTokenAuth
from .errors import error_response
from datetime import datetime


client_token_auth = HTTPTokenAuth()

parser_token_auth = HTTPTokenAuth()


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