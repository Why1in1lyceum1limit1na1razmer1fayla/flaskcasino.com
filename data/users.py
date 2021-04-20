import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, unique=True)
    login = sqlalchemy.Column(sqlalchemy.String)
    password_hash = sqlalchemy.Column(sqlalchemy.String)
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    salt = sqlalchemy.Column(sqlalchemy.String)
    money = sqlalchemy.Column(sqlalchemy.Integer, default=1000)
