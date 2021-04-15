import flask
from flask import request, make_response, render_template

blueprint = flask.Blueprint(
    'casino',
    __name__,
    template_folder='templates',
)


@blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')
