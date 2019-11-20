
import sqlite3

import click
from flask import g, current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
import psycopg2


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(current_app.config['DATABASE_URL'])
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    print(current_app.config['DATABASE_URL'])

    with current_app.open_resource('schema.sql') as f:
        content = f.read().decode('utf8')
        print(content)
        db.cursor().execute(content)
        db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
