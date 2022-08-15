from peewee import SqliteDatabase
from flask import g

def get_db():
    if 'db' not in g:
        g.db = SqliteDatabase("e-commerce-db.db")

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
