from flask import Blueprint, render_template, request, g, flash, redirect, url_for
from auth import login_required
from db import get_db
from budgeting import Budgeting
import peewee

bp = Blueprint('budget', __name__)

@bp.route('/')
def index():
    return render_template("budget/home.html")

@bp.route('/entry', methods=('GET', 'POST'))
@login_required
def new_entry():
    if request.method == 'POST':
        type_entry = request.form["type_entry"]
        if type_entry == "new":
            return redirect(url_for("budget.new_cat"))
        elif type_entry == "existing":
            return redirect(url_for("budget.exis_cat"))
    return render_template("budget/entry.html")

@bp.route('/entry/new',  methods=('GET', 'POST'))
@login_required
def new_cat():
    if request.method == "POST":
        user_id = g.user[0]
        category = request.form["category"]
        method = "Deposit"
        amount = request.form["amount"]
        description = request.form["description"]
        error = None
        db = get_db()

        if not category:
            error = 'Category is required.'
        elif not amount:
            error = 'Amount is required.'

        if error is None:
            try:
                db.execute_sql(
                    "INSERT INTO categories (name) VALUES (?)",
                    (category + "-" + str(user_id),),
                )
            except peewee.IntegrityError:
                error = f"Category {category} has already been created."
            else:
                db.execute_sql(
                    "INSERT INTO entries (user_id, category, method, amount, description) VALUES (?, ?, ?, ?, ?)",
                    (user_id, category, method, amount, description),
                )
                return render_template("budget/success.html", category=category, method=method, amount=amount,
                                       description=description)
        flash(error)
    return render_template("budget/entry_new.html")

@bp.route('/entry/existing',  methods=('GET', 'POST'))
@login_required
def exis_cat():
    db = get_db()
    user_id = g.user[0]
    entry_categories = db.execute_sql("SELECT name FROM categories").fetchall()
    categories = []
    for category in entry_categories:
        cat_tuple = category[0].split("-")
        cat = cat_tuple[0]
        user = cat_tuple[1]
        if user == str(user_id):
            categories.append(cat)
    if request.method == "POST":
        user_id = g.user[0]
        category = request.form["category"]
        method = request.form["method"]
        amount = request.form["amount"]
        description = request.form["description"]
        error = None

        if not category:
            error = 'Category is required.'
        elif not method:
            error = 'Method is required.'
        elif not amount:
            error = 'Amount is required.'

        if method == "Withdraw":
            budget_entries = db.execute_sql(
                "SELECT category, method, amount, description FROM entries WHERE user_id = ?",
                (user_id,)).fetchall()
            cg = Budgeting(category)
            for entry in budget_entries:
                if entry[0] == category:
                    bal_method = entry[1]
                    bal_amount = entry[2]
                    bal_description = entry[3]
                    if bal_method == "Deposit":
                        cg.deposit(int(bal_amount), bal_description)
                    elif bal_method == "Withdraw":
                        cg.withdraw(int(bal_amount), bal_description)
            balance = cg.get_balance()
            if int(amount) > int(balance):
                error = f"Insufficient funds in the {category} category, to withdraw {amount}."

        if error is None:
            db.execute_sql(
                "INSERT INTO entries (user_id, category, method, amount, description) VALUES (?, ?, ?, ?, ?)",
                (user_id, category, method, amount, description),
            )
            return render_template("budget/success.html", category=category, method=method, amount=amount,
                                   description=description)

        flash(error)

    return render_template("budget/entry_exis.html", categories=categories)

@bp.route('/budget/gen')
@login_required
def gen_budget():
    db = get_db()
    user_id = g.user[0]
    budget_entries = db.execute_sql("SELECT category, method, amount, description FROM entries WHERE user_id = ?", (user_id,)).fetchall()
    entry_categories = db.execute_sql("SELECT name FROM categories").fetchall()
    cg_balance = {}

    for category in entry_categories:
        cat_tuple = category[0].split("-")
        cat = cat_tuple[0]
        user = cat_tuple[1]
        if user == str(user_id):
            cg = Budgeting(cat)
            for entry in budget_entries:
                if entry[0] == cat:
                    method = entry[1]
                    amount = entry[2]
                    description = entry[3]
                    if method == "Deposit":
                        cg.deposit(int(amount), description)
                    elif method == "Withdraw":
                        cg.withdraw(int(amount), description)
            values = [cg.deposits, cg.withdrawals, cg.get_balance()]
            cg_balance[cat] = values

    return render_template("budget/budget_gen.html", cg_balance=cg_balance)

@bp.route('/budget/cat/<category>')
@login_required
def cat_budget(category):
    cat = str(category)
    db = get_db()
    user_id = g.user[0]
    budget_entries = db.execute_sql(
        "SELECT category, method, amount, description FROM entries WHERE user_id = ? AND category = ?",
        (user_id, cat)).fetchall()
    cg_deposits = []
    cg_withdrawals = []
    cg = Budgeting(cat)

    for entry in budget_entries:
        method = entry[1]
        amount = entry[2]
        description = entry[3]
        if method == "Deposit":
            cg.deposit(int(amount), description)
            values = [description, amount]
            cg_deposits.append(values)
        elif method == "Withdraw":
            cg.withdraw(int(amount), description)
            values = [description, amount]
            cg_withdrawals.append(values)

    return render_template("budget/budget_cat.html", cg_deposits=cg_deposits, cg_withdrawals=cg_withdrawals,
                           cg_balance=cg.get_balance(), tot_deposits=cg.deposits, tot_withdrawals=cg.withdrawals,
                           category=cat)
