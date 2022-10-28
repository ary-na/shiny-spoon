# from flask import Blueprint, session, redirect, request, abort
# from google.auth.transport import requests
# import os
# import pathlib
# import requests
# from flask import Flask, session, abort, redirect, request
# from google.oauth2 import id_token
# from google_auth_oauthlib.flow import Flow
# from pip._vendor import cachecontrol
# import google.auth.transport.requests
import os
from authlib.integrations.flask_client import OAuth

from flask import Blueprint, url_for, redirect, render_template

from ss.models import LoginForm

auth = Blueprint('auth', __name__, template_folder="templates/ss")
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


# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# GOOGLE_CLIENT_ID = '634070071675-7jodbchjja9bqhk767ivtsn8ms9eac54.apps.googleusercontent.com'
#
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "../shiny_spoon_google_client.json")
#
# flow = Flow.from_client_secrets_file(
#     # Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
#     client_secrets_file=client_secrets_file,
#     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
#             "openid"],
#     # here we are specifying what do we get after the authorization
#     redirect_uri="http://127.0.0.1:5000/callback"
#     # and the redirect URI is the point where the user will end up after the authorization
# )
#
#
# def login_is_required(function):  #a function to check if the user is authorized or not
#     def wrapper(*args, **kwargs):
#         if "google_id" not in session:  #authorization required
#             return abort(401)
#         else:
#             return function()
#
#     return wrapper
#
#
# @auth.route("/login")  #the page where the user can login
# def login():
#     authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
#     session["state"] = state
#     return redirect(authorization_url)
#
#
# @auth.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
# def callback():
#     flow.fetch_token(authorization_response=request.url)
#
#     if not session["state"] == request.args["state"]:
#         abort(500)  #state does not match!
#
#     credentials = flow.credentials
#     request_session = requests.session()
#     cached_session = cachecontrol.CacheControl(request_session)
#     token_request = google.auth.transport.requests.Request(session=cached_session)
#
#     id_info = id_token.verify_oauth2_token(
#         id_token=credentials._id_token,
#         request=token_request,
#         audience=GOOGLE_CLIENT_ID
#     )
#
#     session["google_id"] = id_info.get("sub")  #defing the results to show on the page
#     session["name"] = id_info.get("name")
#     return redirect("/protected_area")  #the final page where the authorized users will end up
#
#
# @auth.route("/logout")  #the logout page and function
# def logout():
#     session.clear()
#     return redirect("/")
#
#
# @auth.route("/")  #the home page where the login button will be located
# def index():
#     return "Hello World <a href='/login'><button>Login</button></a>"
#
#
# @auth.route("/protected_area")  #the page where only the authorized users can go to
# @login_is_required
# def protected_area():
#     return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"  #the logout button


# Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

    return render_template('auth/login.html', form=form)
