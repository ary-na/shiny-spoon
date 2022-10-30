from flask import Flask


def create_app():
    app = Flask(__name__)

    # setup with the configuration provided
    app.config.from_object('config.DevelopmentConfig')
    app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<\!\xd5\xa2\xa0\x9fR"\xa1\xa8'

    # setup all our dependencies

    # blueprint import
    from .auth import auth
    from .views import views

    # register blueprint
    app.register_blueprint(auth)
    app.register_blueprint(views)

    return app
