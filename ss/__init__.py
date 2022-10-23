from flask import Flask


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
