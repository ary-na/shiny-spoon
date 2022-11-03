from flask import Blueprint, render_template

from ss import login_required
from ss.models import Weather

views = Blueprint('views', __name__, template_folder="templates/ss")
weather = Weather()


# Home
@views.route('/')
@login_required
def index():
    # weather_data = weather.get_data()
    return render_template('index.html', weather_condition="weather_data['days'][0]['description']")


# Update account
@views.route('/update-account')
@login_required
def update_account():
    return render_template('account/update.html')


# Delete account
@views.route('/delete-account')
@login_required
def delete_account():
    return render_template('account/delete.html')


# Create post
@views.route('/create-post')
@login_required
def create_post():
    return render_template('post/create.html')


# Update post
@views.route('/update-post')
@login_required
def update_post():
    return render_template('post/update.html')


# Delete post
@views.route('/delete-post')
@login_required
def delete_post():
    return render_template('post/delete.html')
