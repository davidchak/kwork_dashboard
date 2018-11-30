# -*- coding: utf-8 -*-

from flask_security import login_required, roles_required, roles_accepted, current_user
from . import api




############################################################################################################
#     API
############################################################################################################
# TODO: Добавление пользователя                 /api/v1.0/add_user                      - для авторизованного админа
# TODO: Удаление пользователя                   /api/v1.0/del_user                      - для авторизованного админа
# TODO: Добавление парсера                      /api/v1.0/add_parser                    - для авторизованного админа
# TODO: Удаление парсера                        /api/v1.0/del_parser                    - для авторизованного админа
# TODO: Добавление клиента                      /api/v1.0/add_client                    - для авторизованного админа или модератора
# TODO: Удаление клиента                        /api/v1.0/del_client                    - для авторизованного админа или модератора
# TODO: Получение n-последних записей парсера   /api/v1.0/parser/get_last_query/<int>   - для авторизованного админа
# TODO: Получение количества зарег. парсеров    /api/v1.0/parser/get_count              - для авторизованного админа
# TODO: Получение количества зарег. клиентов    /api/v1.0/client/get_count              - для авторизованного админа или модератора
# TODO: Получение количества зарег. модераторов /api/v1.0/moderator/get_count           - для авторизованного админа

# Формат ответа сервера(api):
# api_resp = {
#     'url': '/api/v1.0/add_user',      - url запроса
#     'method': 'POST',                 - метод запроса
#     'success': True,                  - результат выполнения
#     'resp_data': 'data'               - ответ сервера(если нужены какие-либо данные)
#     'error': 'Error'                  - ошибки, если они были
# }


api_resp = {
    'url': '',     
    'method': '',                 
    'success': True,                 
    'resp_data': '',               
    'error': ''                
}


# Добавление пользователя 
@api.route('/api/v1.0/add_user', methods=['POST'])
@roles_required('admin')
def add_user(username, password, role):

    api_resp['url'] = '/api/v1.0/add_user'
    api_resp['method'] = 'POST'

    user = user_datastore.create_user(name=username)
    user.password_hash = generate_password_hash(password)
    try:
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        api_resp['success'] = False
        api_resp['error'] = err

        return jsonify(api_resp)

    role = Role.query.filter_by(name=role).first()
    
    if role:    
        user_datastore.add_role_to_user(user, role)
        
        try:
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            api_resp['success'] = False
            api_resp['error'] = err
        return jsonify(api_resp)
    
    api_resp['success'] = True
    
    return jsonify(api_resp)

    


# Удаление пользователя 
@api.route('/api/v1.0/del_user', methods=['POST'])
@roles_required('admin')
def del_user(username):
    pass


# Добавление парсера 
@api.route('/api/v1.0/add_parser', methods=['POST'])
@roles_required('admin')
def add_parser():
    pass


# Удаление парсера 
@api.route('/api/v1.0/del_parser', methods=['POST'])
@roles_required('admin')
def del_parser(pansername):
    pass


# Добавление клиента 
@api.route('/api/v1.0/add_client', methods=['POST'])
@roles_accepted('admin', 'moderator')
def add_client():
    pass


# Удаление клиента 
@api.route('/api/v1.0/del_client', methods=['POST'])
@roles_accepted('admin', 'moderator')
def del_client(clientname):
    pass


# Получение n-последних записей парсера
@api.route('/api/v1.0/parser/get_last_query/<int:count>', methods=['POST'])
@roles_required('admin')
def get_last_query(count):
    pass


# Получение количества зарег. парсеров
@api.route('/api/v1.0/parser/get_count', methods=['POST'])
@roles_required('admin')
def get_parsers_count():
    pass


# Получение количества зарег. модераторов
@api.route('/api/v1.0/moderator/get_count', methods=['POST'])
@roles_required('admin')
def get_moderators_count():
    pass


# Получение количества зарег. клиентов 
@api.route('/api/v1.0/client/get_count', methods=['POST'])
@roles_accepted('admin', 'moderator')
def get_clients_count():
    pass




# # Удаление пользователя
# @app.route('/del_user', methods=['POST'])
# @login_required
# def del_user():
    
#     user_id = request.form['id']
#     user = User.query.filter_by(id=user_id).first()
    
#     if user:
#         db.session.delete(user)
#         db.session.commit()
    
#         return jsonify({'status': 'success'})
    
#     else:
#         return jsonify({'status': 'error'})


# # Удаление парсера
# @app.route('/del_parser', methods=['POST'])
# @login_required
# def del_parser():

#     parser_id = request.form['id']
#     parser = Parser.query.filter_by(id=parser_id).first()
    
#     if parser:
#         db.session.delete(parser)
#         db.session.commit()
    
#         return jsonify({'status': 'success'})
    
#     else:
#         return jsonify({'status': 'error'})


# # Добавление нового клиента
# @app.route('/add_client', methods=['POST'])
# @login_required
# def add_client():

#     new_client = Client()
#     new_client.name = request.form['client_name']
#     new_client.generate_key()
#     new_client.generate_sicret()
#     count = request.form['days']
#     new_client.extend_life_marker(count)
    
#     try:
#         db.session.add(new_client)
#         db.session.commit()
#         return jsonify({'status': 'success'})
    
#     except:
#         return jsonify({'status': 'error'})


# # API
# @app.route('/api/v1.0/get', methods=['GET','POST'])
# def get_data():
    
#     return jsonify({'status': 'success'})


# @app.route('/api/v1.0/get_last/<count>', methods=['GET'])
# def get_last(count):
    
#     data_list = []
#     data = db.session.query(Data).order_by(Data.id.desc()).limit(count)

#     for item in data:
#         new_item = {
#             'id': item.id,
#             'parser_id': item.parser_id,
#             'datestamp': item.datestamp,
#             'json': item.json
#         }
#         data_list.append(new_item)

#     return jsonify({'result': data_list})


# @app.route('/api/v1.0/set', methods=['POST'])
# def set_data():
    
#     data = request.json
#     result = Parser.query.filter_by(name = data['ID']).first()
    
#     if not result:
#         return jsonify({'status': 'not found parser name'})
    
#     d = Data()
#     d.datestamp = data['datestamp']
#     d.parser_id = data['ID']
#     d.json = str(data['json'])
#     db.session.add(d)
#     db.session.commit() 
    
#     return jsonify({'result': data})


