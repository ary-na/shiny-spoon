import requests as requests
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired


class Logins:

    def __init__(self):
        self.url = 'http://127.0.0.1:8000/logins'

    # async def post(self, user_name, email, password):
    #     paras = {'user_name': user_name, 'email': email, 'password': password}
    #     requests.post(self.url, data=paras)

    def get(self):
        return requests.get(self.url + "/arian")


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
