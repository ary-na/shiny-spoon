import requests as requests
from flask import session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, PasswordField, SubmitField


class Logins:

    def __init__(self):
        self.url = 'http://127.0.0.1:8000/logins/'

    def get_login(self, email):
        return requests.get(self.url + email).json()

    def add_login(self, email, username, password=''):
        data = {'email': email, 'username': username, 'password': password}
        requests.post(self.url + 'add-login', params=data)


# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


# Register form
class SignupForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Get Started')


# Login required
def login_required(function):
    def wrapper(*args, **kwargs):
        if not session.get('email'):
            return redirect(url_for('auth.login'))
        else:
            return function()

    return wrapper
