from flask import Blueprint, render_template, request, session, redirect, flash, g, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import functools
import peewee
from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    db = get_db()

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute_sql('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        firstname = request.form['firstn']
        lastname = request.form['lastn']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        checkbox = request.form['checkbox']
        db = get_db()
        error = None

        if not email:
            error = 'E-mail is required.'
        elif not username:
            error = 'Username is required.'
        elif not firstname or not lastname:
            error = 'Full name is required.'
        elif not password:
            error = 'Password is required.'
        elif not password == confirm_password:
            error = 'Password confirmation does not match.'
        elif not checkbox:
            error = 'You must accept the Terms and Conditions.'

        if error is None:
            try:
                db.execute_sql(
                    "INSERT INTO users (username, password, email, firstn, lastn) VALUES (?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), email, firstname, lastname),
                )
            except peewee.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)

    return render_template("auth/register.html")

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        login_user = db.execute_sql('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if login_user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(str(login_user[2]), password):
            error = 'Incorrect password.'

        if error is None:
            session['user_id'] = login_user[0]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")

@bp.route('/logout')
@login_required
def logout():
    del session['user_id']
    return redirect(url_for("index"))
