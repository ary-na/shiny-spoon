import os

import requests as requests
from flask_wtf import FlaskForm
from flask import session, redirect, url_for
from wtforms.validators import InputRequired
from wtforms import StringField, PasswordField, SubmitField


# Logins
class Logins:

    def __init__(self):
        self.url = 'http://127.0.0.1:8000/logins/'

    # Create login
    def add_login(self, email, username, password=''):
        data = {'email': email, 'username': username, 'password': password}
        requests.post(self.url + 'add-login', params=data)

    # Read login
    def get_login(self, email):
        return requests.get(self.url + email).json()

    # Update login
    def update_login(self):
        data = {}
        return requests.put(self.url + 'update-login', params=data)

    # Delete login
    def delete_login(self, email):
        data = {}
        return requests.delete(self.url + 'update-login', params=data)


# Posts
class Posts:
    def __int__(self):
        self.url = 'http://127.0.0.1:8000/posts/'

    # Create post
    def add_post(self, email, username, password=''):
        data = {'email': email, 'username': username, 'password': password}
        requests.post(self.url + 'add-post', params=data)

    # Read post
    def get_post(self, email):
        return requests.get(self.url + email).json()

    # Update post
    def update_post(self):
        data = {}
        return requests.put(self.url + 'update-post', params=data)

    # Delete post
    def delete_post(self, email):
        data = {}
        return requests.delete(self.url + 'update-post', params=data)


# Weather
class Weather:

    def __init__(self):
        self.key = "update the key later"
        self.url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Melbourne' \
                   '/today?unitGroup=us&include=days&key=' + self.key + '&contentType=json'

    def get_data(self):
        return requests.get(self.url).json()


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
