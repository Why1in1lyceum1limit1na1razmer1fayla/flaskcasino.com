from flask import Flask
from data import db_session, users_api
from config import config

app = Flask(__name__)


def main(config_name='default'):
    app.config.from_object(config[config_name])
    db_session.global_init("db/db.db")
    app.register_blueprint(users_api.blueprint)
    app.run()


if __name__ == '__main__':
    main('development')
