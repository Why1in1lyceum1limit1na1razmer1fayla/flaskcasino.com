import flask
from flask import request, make_response, render_template, redirect
from . import db_session
from .users import User
import hashlib
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import login_user

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates',
)


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Пароль еще раз(на всякий случай, мало ли опечатку допустили, мы за вас переживаем)',
        validators=[DataRequired()])
    license_confirm = BooleanField(
        'Я не имею претензий к НКО "Коммерческий фонд манулов Ярослава и Матвея", '
        'даже если имею подозрения что игра идет не совсем честно', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')

    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')

    submit = SubmitField('Войти')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        session = db_session.create_session()
        try:
            login = form.username.data
            password = form.password.data
            user = session.query(User).filter(User.login == login).first()
            if user.password_hash == hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                                         user.salt, 20000):
                session.close()
                print(user)
                login_user(user, remember=form.remember_me.data)

                return redirect('/profile')
            else:
                session.close()
                return render_template('login.html', message=[
                    'Вы ввели что-то не то, пожалуйста, будьте внимательнее и попробуйте еще раз!'], form=form)
        except:
            session.close()
            return render_template('login.html', message=[
                'Вы ввели что-то не то, пожалуйста, будьте внимательнее и попробуйте еще раз!'], form=form)


@blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('registration.html', form=form)
    else:

        if form.validate_on_submit():

            session = db_session.create_session()  # Подключаемся к БД
            try:
                login = form.username.data
                password = form.password.data
                is_confim_logined = form.remember_me.data
                if not session.query(User).filter(
                        User.login == login).first() and password == form.confirm_password.data:
                    user = User()
                    salt = os.urandom(32)
                    user.login = login
                    user.salt = salt
                    user.password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                                             salt, 20000)
                    session.add(user)
                    session.commit()
                    session.close()
                    user = session.query(User).filter(User.login == login).first()
                    login_user(user, remember=form.remember_me.data)
                    return redirect('/profile')
                else:
                    session.close()
                    return render_template('registration.html', message=[
                        'Такой пользователь уже существует!'], form=form)
            except:
                session.close()
                return render_template('registration.html', message=[
                    'Вы ввели что-то не то, пожалуйста, будьте внимательнее и попробуйте еще раз!'], form=form)
        else:
            return render_template('login.html', form=form)
