from flask import Flask, render_template, request, session, redirect, flash, g
from peewee import SqliteDatabase
from werkzeug.security import check_password_hash, generate_password_hash
import functools
import peewee

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev',)

budget_db = SqliteDatabase("budget_db.db")
budget_db.connect()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/login")
        return view(**kwargs)
    return wrapped_view

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = budget_db.execute_sql('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

@app.route('/')
def welcome():
    return render_template("home.html")

@app.route('/budget', methods=('GET', 'POST'))
def welcome_budget():
    if request.method == 'POST':
        user_id = g.user[0]
        category = request.form["category"]
        method = request.form["method"]
        amount = request.form["amount"]
        description = request.form["description"]
        budget_db.execute_sql(
            "INSERT INTO entries (user_id, category, method, amount, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, category, method, amount, description),
        )

        return render_template("entry_success.html", category=category, method=method, amount=amount, description=description)
    elif request.method == 'GET':
        return render_template("budget.html")

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            try:
                budget_db.execute_sql(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
            except peewee.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return render_template("reg_success.html", username=username, password=password)
        flash(error)

    return render_template("register.html")

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        login_user = budget_db.execute_sql('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if login_user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(str(login_user[2]), password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = login_user[0]
            return render_template("login_success.html", username=username, password=password)

        flash(error)

    return render_template("login.html")

@app.route('/logout', )
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
