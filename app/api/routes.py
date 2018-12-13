# -*- coding: utf-8 -*-

from flask import jsonify, request, current_app
from flask_security import login_required, roles_required, roles_accepted, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import api
from app import db
from app.models import Data, User, Parser, Client, Role
from .auth import client_token_auth, parser_token_auth
from datetime import datetime


@api.route('/api/v1.0/client/get_data/<int:count>', methods=['GET'])
@client_token_auth.login_required
def get_client_data(count):
    

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    api_resp['url'] = '/api/v1.0/client/get_data/<count>'
    api_resp['method'] = 'GET'

    data_list = []
    data = db.session.query(Data).order_by(Data.id.desc()).limit(count)

    for item in data:
        new_item = {
            'id': item.id,
            'parser_id': item.parser_id,
            'datestamp': item.datestamp,
            'json': item.json
        }
        data_list.append(new_item)

    api_resp['success'] = True
    api_resp['resp_data'] = data_list

    return jsonify(api_resp)


@api.route('/api/v1.0/parser/set_data', methods=['POST'])
@parser_token_auth.login_required
def set_parser_data():

    format = r"%Y-%m-%d %H:%M:%S"
    
    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    data = request.json


    api_resp['url'] = '/api/v1.0/parser/set_data'
    api_resp['method'] = 'POST'

    parser = Parser.query.filter_by(token=data['token']).first()

    if parser:
        parser.set_data(datestamp=datetime.strptime(data['datestamp'][:-7], format), json=str(data['json']))
        api_resp['success'] = True
    else:
        api_resp['success'] = False

    return jsonify(api_resp)
