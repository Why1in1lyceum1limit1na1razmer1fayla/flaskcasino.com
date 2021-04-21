import flask
from flask import request, make_response, render_template
from flask_login import current_user

blueprint = flask.Blueprint(
    'casino',
    __name__,
    template_folder='templates',
)


@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@blueprint.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html', current_user=current_user)
