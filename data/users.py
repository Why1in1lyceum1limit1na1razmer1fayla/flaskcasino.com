import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin, current_user


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, unique=True)
    login = sqlalchemy.Column(sqlalchemy.String)
    password_hash = sqlalchemy.Column(sqlalchemy.String)
    salt = sqlalchemy.Column(sqlalchemy.String)
    money = sqlalchemy.Column(sqlalchemy.Integer, default=1000)


def get_user_login():
    return current_user.login


def get_user_money():
    return current_user.money


def get_user_id():
    return current_user.id
