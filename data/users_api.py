import flask
from flask import request, make_response
import db_session
from users import User
import hashlib
import os

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates',
    url_prefix='/users',
)


@blueprint.route('/create_user', methods=['POST'])
def create_user():
    session = db_session.create_session()  # Подключаемся к БД
    try:
        data = request.json
        login = data['login']
        name = data['name']
        password = data['password']
        try:
            weight = data['weight']
        except KeyError:
            weight = None
        try:
            age = data['age']
        except KeyError:
            age = None
        if not session.query(User).filter(User.login == login).first():
            user = User()
            salt = os.urandom(32)
            user.login = login
            user.name = name
            user.weight = weight
            user.age = age
            user.salt = salt
            user.password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                                     salt, 20000)
            session.add(user)
            session.commit()
            session.close()
            return make_response({'successful': 'user created'}, 201)
        else:
            session.close()
            return make_response({'error': 'user already exists'}, 400)
    except:
        session.close()
        return make_response({'error': 'server_error'}, 500)


@blueprint.route('/login_user', methods=['POST'])
def login_user():
    session = db_session.create_session()
    try:
        data = request.json
        login = data['login']
        password = data['password']
        user = session.query(User).filter(User.login == login).first()
        if user.password_hash == hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                                     user.salt, 20000):
            session.close()
            return make_response({'successful': 'user logined'}, 201)
        else:
            session.close()
            return make_response({'error': 'user not logined'}, 401)
    except:
        session.close()
        return make_response({'error': 'server_error'}, 500)
