import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

import os
from google.cloud import storage

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def dump_db():
    bucket_name = os.environ.get('BUCKET_NAME', None)
    filename = 'schema.sql'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)

    db = get_db()
    with blob.open(mode='w', encoding='UTF-8') as blob_source:
        for line in db.iterdump():
            blob_source.write(f'{line}\n')


def restore_db():
    bucket_name = os.environ.get('BUCKET_NAME', None)
    filename = 'schema.sql'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)

    with sqlite3.connect(
                     current_app.config['DATABASE'],
                     detect_types=sqlite3.PARSE_DECLTYPES
                 ) as db
        db.row_factory = sqlite3.Row

        with blob.open(mode='r', encoding='UTF-8') as blob_source:
            db.executescript(blob_source.read().decode('utf8'))


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)