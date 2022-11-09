import pytz
import requests as requests
from dateutil import tz
from dateutil import parser
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField


# Logins
class Logins:

    def __init__(self):
        self.url = 'http://127.0.0.1:8000/logins/'

    # Create login
    def add_login(self, email, username, password=''):
        data = {'email': email, 'username': username, 'password': password, 'img_key': 'default-user-profile-img'
                                                                                       '-white.png'}
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
    def __init__(self):
        self.url = 'http://127.0.0.1:8000/posts/'

    # Create post
    def add_post(self, email, description, post_img_key):
        data = {'email': email, 'description': description, 'post_img_key': post_img_key}
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

    def get_user_posts(self, email):
        return requests.get(self.url + email).json()

    def get_posts(self):
        return requests.get(self.url).json()


# Weather
class Weather:

    def __init__(self):
        self.key = "update the key later"
        self.url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Melbourne' \
                   '/today?unitGroup=us&include=days&key=' + self.key + '&contentType=json'

    def get_data(self):
        return requests.get(self.url).json()


# Utilities
class Utilities:

    def __init__(self):
        self.url = 'http://127.0.0.1:8000/utilities/'

    # Upload profile image
    def upload_profile_img(self, img_file, object_key):
        data = {'object_key': object_key}
        image = {'img_file': img_file}
        requests.post(self.url + 'upload-profile-img', params=data, files=image)

    # Upload post image
    def upload_post_img(self, img_file, object_key):
        data = {'object_key': object_key}
        image = {'img_file': img_file}
        requests.post(self.url + 'upload-post-img', params=data, files=image)

    # Get pre-signed url profile image
    def get_pre_signed_url_profile_img(self, object_key):
        return requests.get(self.url + 'profile-img/' + object_key).json()

    # Get pre-signed url post image
    def get_pre_signed_url_post_img(self, object_key):
        return requests.get(self.url + 'post-img/' + object_key).json()


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


# Create post form
class CreatePostForm(FlaskForm):
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Add Image')
    submit = SubmitField('Create')


# Change password form
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Submit')


# Update profile image form
class UpdateProfileImageForm(FlaskForm):
    image = FileField('Add Image', validators=[InputRequired()])
    submit = SubmitField('Update')


# Convert date time utc to local time
def convert_date_time_utc_to_local(date_time_utc_string):
    date_time_utc_object = parser.parse(date_time_utc_string)
    date_time_local_object = date_time_utc_object.replace(tzinfo=pytz.utc).astimezone(tz.tzlocal())
    date_time_local_formatted = date_time_local_object.strftime('%d/%m/%Y %H:%M')
    return date_time_local_formatted
