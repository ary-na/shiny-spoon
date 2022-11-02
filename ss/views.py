from flask import Blueprint, render_template

from ss.models import login_required

views = Blueprint('views', __name__, template_folder="templates/ss")


# Home
@views.route('/')
@login_required
def index():
    return render_template('index.html')


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
