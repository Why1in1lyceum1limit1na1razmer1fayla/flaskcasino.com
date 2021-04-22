import flask
from flask import render_template, request
from .users import get_user_login
from random import randint, choice

blueprint = flask.Blueprint(
    'mark123',
    __name__,
    template_folder='templates',
)



class MarkGame():
    def __init__(self):
        name = get_user_login()
        r_number = randint(1, 101)
        pl_num = "число игрока"
        if "mark" in name.lower() and 'lox' not in name.lower():
            r_number = pl_num
        if "grisha" in name.lower() and 'lox' not in name.lower():
            r_number = "лох"

        if pl_num == r_number:
            if choice([0, 1, 1, 1, 1]) == 1:
                self.win()
            else:
                self.lose()
        else:
            self.lose()

    def win(self):
        pass

    def lose(self):
        pass


@blueprint.route('/mark123game', methods=['GET', 'POST'])
def gaming():
    if request.method == 'GET':
        return render_template('mark123.html')