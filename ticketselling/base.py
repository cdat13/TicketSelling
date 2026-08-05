from dynaconf import FlaskDynaconf
from flask import Flask


def create_app(**config):
    app = Flask(__name__)
    FlaskDynaconf(app)

    app.config.load_extensions("EXTENSIONS")
    app.config.update(config)

    print("=" * 60)
    print("DATABASE URI:")
    print(app.config.get("SQLALCHEMY_DATABASE_URI"))
    print("=" * 60)

    return app


def create_app_wsgi():
    app = create_app()
    return app