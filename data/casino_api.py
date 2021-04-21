import flask
from flask import request, make_response, render_template
from flask_login import current_user, login_required
from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'casino',
    __name__,
    template_folder='templates',
)


@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@login_required
@blueprint.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html', current_user=current_user)


@login_required
@blueprint.route('/leaders', methods=['GET'])
def leaders():
    session = db_session.create_session()
    users = session.query(User).order_by(User.money).all()[::-1]
    return render_template('leaders.html', users=users)
