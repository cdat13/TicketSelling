from dynaconf import FlaskDynaconf
from flask import Flask


def create_app(**config):
       app = Flask(__name__)
    FlaskDynaconf(app)

    print("=" * 50)
    print("Current ENV:", app.config.current_env)
    print("Database URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))
    print("=" * 50)

    app.config.load_extensions("EXTENSIONS")
    app.config.update(config)
    return app

def create_app_wsgi():
    # workaround for Flask issue
    # that doesn't allow **config
    # to be passed to create_app
    # https://github.com/pallets/flask/issues/4170
    app = create_app()
    return app
