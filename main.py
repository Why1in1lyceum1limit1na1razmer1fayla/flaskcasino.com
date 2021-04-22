from flask import Flask, render_template
from data import db_session, users_api, casino_api, Guess_the_number
from config import config
from flask_login import LoginManager
from data.users import User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main(config_name='default'):
    app.config.from_object(config[config_name])
    db_session.global_init("db/db.db")
    app.register_blueprint(users_api.blueprint)
    app.register_blueprint(casino_api.blueprint)
    app.register_blueprint(Guess_the_number.blueprint)
    app.run()


if __name__ == '__main__':
    main('development')
