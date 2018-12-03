# -*- coding: utf-8 -*-

from flask import jsonify, request, current_app
from flask_security import login_required, roles_required, roles_accepted, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import api
from app import db
from app.models import Data, User, Parser, Client, Role
from .auth import client_token_auth, parser_token_auth



############################################################################################################
#     API для парсеров и клиентов
############################################################################################################
# TODO: Получение информации для клиентов           /api/v1.0/client/get_data   GET
# TODO: Отправка данных в базу для зарег.парсера    /api/v1.0/parser/set_data   POST


@api.route('/api/v1.0/client/get_data/<int:count>', methods=['GET'])
@client_token_auth.login_required
def get_client_data(count):
    return jsonify({'success': True})


@api.route('/api/v1.0/parser/set_data', methods=['POST'])
@parser_token_auth.login_required
def set_parser_data():
    pass