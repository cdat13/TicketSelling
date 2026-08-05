import click

from ticketselling.ext.auth import create_user
from ticketselling.ext.database import db
from ticketselling.seed_data import seed_data


@click.command("create-db")
def create_db():
    """Tạo database"""
    db.create_all()
    click.echo("Database created.")


@click.command("drop-db")
def drop_db():
    """Xóa database"""
    db.drop_all()
    click.echo("Database dropped.")


@click.command("seed")
def seed():
    """Seed dữ liệu mẫu"""
    seed_data()
    click.echo("Seed completed.")


def init_app(app):
    app.cli.add_command(create_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(seed)

    @app.cli.command("add-user")
    @click.option("--full-name", required=True)
    @click.option("--email", required=True)
    @click.option("--username", required=True)
    @click.option("--password", required=True)
    def add_user(full_name, email, username, password):
        create_user(
            full_name=full_name,
            email=email,
            username=username,
            password=password,
        )