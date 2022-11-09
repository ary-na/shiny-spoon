import uuid

from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from ss import login_required
from ss.models import Weather, CreatePostForm, Utilities, Posts, Logins, convert_date_time_utc_to_local, \
    UpdateAccountForm, DeleteAccountForm, UpdatePostForm

posts = Posts()
logins = Logins()
weather = Weather()
utilities = Utilities()
views = Blueprint('views', __name__, template_folder="templates/ss")


# Home
@views.route('/')
@login_required
def index():
    # weather_data = weather.get_data()
    user = logins.get_login(session['email'])
    latest_posts = posts.get_posts()

    return render_template('index.html',
                           user=user[0],
                           posts=latest_posts,
                           weather_condition="weather_data['days'][0]['description']",
                           get_pre_signed_url_profile_img=utilities.get_pre_signed_url_profile_img,
                           get_pre_signed_url_post_img=utilities.get_pre_signed_url_post_img,
                           convert_date_time_utc_to_local=convert_date_time_utc_to_local)


# User account
@views.route('/user-account')
@login_required
def user_account():
    user = logins.get_login(session['email'])
    user_posts = posts.get_user_posts(user[0]['email'])
    return render_template('account/user.html',
                           user=user[0],
                           posts=user_posts,
                           get_pre_signed_url_profile_img=utilities.get_pre_signed_url_profile_img,
                           get_pre_signed_url_post_img=utilities.get_pre_signed_url_post_img,
                           convert_date_time_utc_to_local=convert_date_time_utc_to_local)


# Update account
@views.route('/update-account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    user = logins.get_login(session['email'])

    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        image = request.files['image']

        if not old_password and not new_password and not image:
            flash('Input required', 'error')

        if new_password and old_password and old_password == user[0]['password']:
            logins.update_login_password(user[0]['email'], user[0]['username'], new_password)
            flash('Password successfully changed', 'success')
        elif old_password or new_password and old_password != user[0]['password']:
            flash('Old password is incorrect', 'error')

        if image:
            profile_image_key = str(uuid.uuid4()) + image.filename
            utilities.upload_profile_img(image, profile_image_key)
            logins.update_login_image_key(user[0]['email'], user[0]['username'], profile_image_key)
            user = logins.get_login(session['email'])
            flash('Profile image successfully updated', 'success')

    return render_template('account/update.html', user=user[0], form=form,
                           get_pre_signed_url_profile_img=utilities.get_pre_signed_url_profile_img)


# Delete account
@views.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        user = logins.get_login(session['email'])
        user_posts = posts.get_user_posts(user[0]['email'])

        for post in user_posts:
            posts.update_post_active_state(user[0]['email'], post['date_time_utc'])

        logins.delete_login(user[0]['email'], user[0]['username'])
        return redirect(url_for('auth.logout'))

    return render_template('account/delete.html', form=form)


# Create post
@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    user = logins.get_login(session['email'])

    if form.validate_on_submit():
        description = form.description.data
        image = request.files['image']
        post_image_key = ''

        if image:
            post_image_key = str(uuid.uuid4()) + image.filename
            utilities.upload_post_img(image, post_image_key)

        posts.add_post(user[0]['email'], user[0]['username'], user[0]['img_key'], description, post_image_key)
        return redirect(url_for('views.index'))

    return render_template('post/create.html', form=form)


# Update post
@views.route('/update-post/<post_date_time_utc>', methods=['GET', 'POST'])
@login_required
def update_post(post_date_time_utc):
    form = UpdatePostForm()
    post = posts.get_post(session['email'], post_date_time_utc)

    if form.validate_on_submit():
        description = form.description.data
        image = request.files['image']

        if image:
            post_image_key = str(uuid.uuid4()) + image.filename
            utilities.upload_post_img(image, post_image_key)
        else:
            post_image_key = post['post_img_key']

        posts.update_post(post['email'], post_date_time_utc, description, post_image_key)
        return redirect(url_for('views.user_account'))

    form.description.data = post['description']
    return render_template('post/update.html',
                           form=form,
                           post=post,
                           get_pre_signed_url_post_img=utilities.get_pre_signed_url_post_img)


# Delete post
@views.route('/delete-post/<post_date_time_utc>')
@login_required
def delete_post(post_date_time_utc):
    posts.delete_post(session['email'], post_date_time_utc)
    return redirect(url_for('views.user_account'))
