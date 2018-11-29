# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, jsonify, abort, Response
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash
from flask_security import login_required, current_user, roles_required, roles_accepted
from .models import User, Data, Parser, LoginForm, AddUserForm, NewParserForm, Client
from . import app, db, user_datastore

############################################################################################################
#     ROUTES
############################################################################################################

@app.route('/login', methods=['GET', 'POST'])
def login():  
    
    form = LoginForm()
    message = ''
    
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data.lower()).first()
    
        if user is None or not user.check_password(form.password.data):
            message = u'Проверите правильность ввода логина или пароля!'
    
            return redirect(url_for('login'))
    
        login_user(user)
 
        if current_user.has_role('admin'):
            return redirect(url_for('get_admin_page', username=user.name))
        elif current_user.has_role('moderator'):
            return redirect(url_for('get_moderator_page', username=user.name))
    
    return render_template('login.html', form = form)


# Выход
@app.route("/logout")
def logout():
    
    logout_user()
    return redirect(url_for('login'))


# Админка
@app.route('/admin_panel/<username>', methods=['GET', 'POST'])
@roles_required('admin')
def get_admin_page(username):

    return render_template('admin.html')


# Модераторка
@app.route('/moderator_panel/<username>', methods=['GET', 'POST'])
@roles_required('moderator')
def get_moderator_page(username):
    
    return render_template('moderator.html')



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
    'resp_data': ''               
    'error': ''                
}


# Добавление пользователя 
@app.route('/api/v1.0/add_user', methods=['POST'])
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
@app.route('/api/v1.0/del_user', methods=['POST'])
@roles_required('admin')
def del_user(username):
    pass


# Добавление парсера 
@app.route('/api/v1.0/add_parser', methods=['POST'])
@roles_required('admin')
def add_parser():
    pass


# Удаление парсера 
@app.route('/api/v1.0/del_parser', methods=['POST'])
@roles_required('admin')
def del_parser(pansername):
    pass


# Добавление клиента 
@app.route('/api/v1.0/add_client', methods=['POST'])
@roles_accepted('admin', 'moderator')
def add_client():
    pass


# Удаление клиента 
@app.route('/api/v1.0/del_client', methods=['POST'])
@roles_accepted('admin', 'moderator')
def del_client(clientname):
    pass


# Получение n-последних записей парсера
@app.route('/api/v1.0/parser/get_last_query/<int:count>', methods=['POST'])
@roles_required('admin')
def get_last_query(count):
    pass


# Получение количества зарег. парсеров
@app.route('/api/v1.0/parser/get_count', methods=['POST'])
@roles_required('admin')
def get_parsers_count():
    pass


# Получение количества зарег. модераторов
@app.route('/api/v1.0/moderator/get_count', methods=['POST'])
@roles_required('admin')
def get_moderators_count():
    pass


# Получение количества зарег. клиентов 
@app.route('/api/v1.0/client/get_count', methods=['POST'])
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




############################################################################################################
#     ERRORS
############################################################################################################
# TODO: Зарегистрировать страницу ошибки 404
# TODO: Зарегистрировать страницу ошибки 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500