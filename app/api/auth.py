# -*- coding: utf-8 -*-

from flask import g
from app.models import Client, Parser
from flask_httpauth import HTTPTokenAuth
from .errors import error_response


client_token_auth = HTTPTokenAuth()

parser_token_auth = HTTPTokenAuth()


@client_token_auth.verify_token
def verify_token(token):
    g.current_user = Client.check_token(token) if token else None
    return g.current_user is not None


@client_token_auth.error_handler
def token_auth_error():
    return error_response(401)


@parser_token_auth.verify_token
def verify_token(token):
    g.current_user = Parser.check_token(token) if token else None
    return g.current_user is not None
