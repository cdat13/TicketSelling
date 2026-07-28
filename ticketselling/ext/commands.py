import click

from ticketselling.ext.auth import create_user
from ticketselling.ext.database import db
from ticketselling.seed_data import seed_data


def create_db():
    """Creates database"""
    db.create_all()
    seed_data()

    click.echo("Đã tạo database và thêm dữ liệu mẫu")


def drop_db():
    """Cleans database"""
    db.drop_all()


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db]:
        app.cli.add_command(app.cli.command()(command))

    # add a single command
    @app.cli.command()
    @click.option("--username", "-u")
    @click.option("--password", "-p")
    def add_user(full_name,email,username, password):
        """Adds a new user to the database"""
        return create_user(full_name=full_name, email=email,username=username, password=password)
