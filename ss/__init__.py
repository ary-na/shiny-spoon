from functools import wraps

from flask import Flask, session, redirect, url_for


# Login required
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('email'):
            return redirect(url_for('auth.login'))
        else:
            return f(*args, **kwargs)

    return wrap


def create_app():
    app = Flask(__name__)

    # setup with the configuration provided
    app.config.from_object('config.DevelopmentConfig')

    # setup all our dependencies

    # blueprint import
    from .auth import auth
    from .views import views

    # register blueprint
    app.register_blueprint(auth)
    app.register_blueprint(views)

    return app
