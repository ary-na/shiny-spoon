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

    # Update login password
    def update_login_password(self, email, username, new_password):
        data = {'email': email, 'username': username, 'password': new_password}
        requests.put(self.url + 'update-login-password', params=data)

    # Update login profile image
    def update_login_profile_image(self, email, username, new_img_key):
        data = {'email': email, 'username': username, 'img_key': new_img_key}
        requests.put(self.url + 'update-login-profile-image', params=data)

    # Delete login
    def delete_login(self, email, username):
        data = {'email': email, 'username': username}
        return requests.delete(self.url + 'delete-login', params=data)


# Posts
class Posts:
    def __init__(self):
        self.url = 'http://127.0.0.1:8000/posts/'

    # Create post
    def add_post(self, email, username, user_profile_img_key, description, post_img_key):
        data = {'email': email, 'username': username, 'user_profile_img_key': user_profile_img_key,
                'description': description, 'post_img_key': post_img_key}
        requests.post(self.url + 'add-post', params=data)

    # Read post
    def get_post(self, email, date_time_utc):
        return requests.get(self.url + email + '/' + date_time_utc).json()

    # Update post
    def update_post(self, email, date_time_utc, description, post_img_key):
        data = {'email': email, 'date_time_utc': date_time_utc, 'description': description,
                'post_img_key': post_img_key}
        return requests.put(self.url + 'update-post', params=data)

    # Update post active state
    def update_post_active_state(self, email, date_time_utc):
        data = {'email': email, 'date_time_utc': date_time_utc}
        return requests.put(self.url + 'update-post-active-state', params=data)

    # Delete post
    def delete_post(self, email, date_time_utc):
        data = {'email': email, 'date_time_utc': date_time_utc}
        return requests.delete(self.url + 'delete-post', params=data)

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


# Update post form
class UpdatePostForm(FlaskForm):
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Update Image')
    submit = SubmitField('Update')


# Update Account form
class UpdateAccountForm(FlaskForm):
    old_password = PasswordField('Old Password')
    new_password = PasswordField('New Password')
    image = FileField('Update Image')
    submit = SubmitField('Update')


# Delete Account form
class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Delete Account')


# Convert date time utc to local time
def convert_date_time_utc_to_local(date_time_utc_string):
    date_time_utc_object = parser.parse(date_time_utc_string)
    date_time_local_object = date_time_utc_object.replace(tzinfo=pytz.utc).astimezone(tz.tzlocal())
    date_time_local_formatted = date_time_local_object.strftime('%d/%m/%Y %H:%M')
    return date_time_local_formatted
