import uuid

from flask import Blueprint, render_template, request, session, redirect, url_for

from ss import login_required
from ss.models import Weather, CreatePostForm, Utilities, Posts

posts = Posts()
weather = Weather()
utilities = Utilities()
post_images_folder = 'post-images/'
user_images_folder = 'user-images/'
views = Blueprint('views', __name__, template_folder="templates/ss")


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
@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post_id = str(uuid.uuid4())
        description = form.description.data
        image = request.files['image']
        post_image_key = ''
        if image:
            post_image_key = post_id + image.filename
            utilities.upload_img(image, post_image_key, post_images_folder)

        posts.add_post(session.get('email'), post_id, description, post_image_key)
        return redirect(url_for('views.index'))

    return render_template('post/create.html', form=form)


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
