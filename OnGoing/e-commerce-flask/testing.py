from flask import Blueprint, session
from peewee import SqliteDatabase

bp = Blueprint('testing', __name__)

@bp.route('/testing')
def testing():
    return session
