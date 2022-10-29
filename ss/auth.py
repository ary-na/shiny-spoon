import os
import os.path
import pathlib
import requests
import google.auth.transport.requests
from google.oauth2 import id_token
from pip._vendor import cachecontrol
from google_auth_oauthlib.flow import Flow
from ss.models import LoginForm, SignupForm, Logins
from flask import Blueprint, url_for, redirect, render_template, session, flash, abort, request

# oauth = OAuth(app)
#
#
# @auth.route('/facebook')
# def facebook():
#     # Facebook Oauth Config
#     FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID')
#     FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET')
#     oauth.register(
#         name='facebook',
#         client_id=FACEBOOK_CLIENT_ID,
#         client_secret=FACEBOOK_CLIENT_SECRET,
#         access_token_url='https://graph.facebook.com/oauth/access_token',
#         access_token_params=None,
#         authorize_url='https://www.facebook.com/dialog/oauth',
#         authorize_params=None,
#         api_base_url='https://graph.facebook.com/',
#         client_kwargs={'scope': 'email'},
#     )
#     redirect_uri = url_for('facebook_auth', _external=True)
#     return oauth.facebook.authorize_redirect(redirect_uri)
#
#
# @auth.route('/facebook/auth/')
# def facebook_auth():
#     token = oauth.facebook.authorize_access_token()
#     resp = oauth.facebook.get(
#         'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
#     profile = resp.json()
#     print("Facebook User ", profile)
#     return redirect('/')

logins = Logins()
auth = Blueprint('auth', __name__, template_folder='templates/ss')
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, '../shiny_spoon_google_client.json')
flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
                                     scopes=['https://www.googleapis.com/auth/userinfo.profile',
                                             'https://www.googleapis.com/auth/userinfo.email',
                                             'openid'],
                                     redirect_uri='http://127.0.0.1:5000/callback'
                                     )


# Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = logins.get_login(email)
        if user and user[0]['password'] == password:
            session['email'] = user[0]['email']
            session['username'] = user[0]['username']
            return redirect(url_for('views.wrapper'))
        else:
            flash('Email or password is invalid')

    return render_template('auth/login.html', form=form)


# Register
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        user_exists = logins.get_login(email)
        if not user_exists:
            logins.add_login(email, username, password)
            session['email'] = email
            session['username'] = username
            return redirect(url_for('views.wrapper'))
        else:
            flash('The email already exists')

    return render_template('auth/signup.html', form=form)


# Google login
@auth.route('/google-login')
def google_login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)


# Google callback
@auth.route('/callback')
def google_callback():
    flow.fetch_token(authorization_response=request.url)

    if not session['state'] == request.args['state']:
        abort(500)  # state does not match

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=os.environ.get('GOOGLE_CLIENT_ID')
    )

    user_exists = logins.get_login(id_info.get('email'))
    if not user_exists:
        logins.add_login(id_info.get('email'), id_info.get('name'))

    session['email'] = id_info.get('email')
    session['username'] = id_info.get('name')
    return redirect(url_for('views.wrapper'))


# Logout
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
