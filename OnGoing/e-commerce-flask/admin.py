from flask import Blueprint, render_template, request, flash, redirect, url_for
from auth import login_required
from db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@login_required
def dashboard():
    return render_template("admin/index.html")

@bp.route('/products')
@login_required
def products():
    db = get_db()
    product_entries = db.execute_sql(
        "SELECT id, name, category, brand, price FROM products").fetchall()

    return render_template("admin/products.html", product_entries=product_entries)

@bp.route('/products/new', methods=('GET', 'POST'))
@login_required
def new_prod():
    if request.method == "POST":
        name = request.form["product-name"]
        category = request.form["category"]
        brand = request.form["brand"]
        price = request.form["price"]
        description = request.form["product-details"]
        db = get_db()
        error = None

        if not name:
            error = 'Product name is required.'
        elif not category:
            error = 'Product category is required.'
        elif not brand:
            error = 'Product brand is required.'
        elif not price:
            error = 'Product price is required.'
        elif not description:
            error = 'Product description is required.'
        elif len(str(description)) < 10:
            error = 'The description is less than 10 characters long.'

        if not error:
            db.execute_sql(
                    "INSERT INTO products (name, category, brand, price, desc) VALUES (?, ?, ?, ?, ?)",
                    (name, category, brand, price, description),
                )
            flash("Product creation has been successful.")
        else:
            flash(error)
    return render_template("admin/new_prod.html")

@bp.route('/products/edit/<p_id>', methods=('GET', 'POST'))
@login_required
def edit_prod(p_id):
    db = get_db()
    product_id = p_id
    product = db.execute_sql(
        "SELECT name, category, brand, price, desc FROM products WHERE id = ?", (product_id,)).fetchone()
    name = product[0]
    category = product[1]
    brand = product[2]
    price = product[3]
    description = product[4]

    if request.method == "POST":
        name = request.form["product-name"]
        category = request.form["category"]
        brand = request.form["brand"]
        price = request.form["price"]
        description = request.form["product-details"]
        error = None

        if not name:
            error = 'Product name is required.'
        elif not category:
            error = 'Product category is required.'
        elif not brand:
            error = 'Product brand is required.'
        elif not price:
            error = 'Product price is required.'
        elif not description:
            error = 'Product description is required.'
        elif len(str(description)) < 10:
            error = 'The description is less than 10 characters long.'

        if not error:
            db.execute_sql(
                    "UPDATE products SET name = ?, category = ?, brand = ?, price = ?, desc = ? WHERE id = ?;",
                    (name, category, brand, price, description, product_id),
                )
            flash("Product has been successfully updated.")
        else:
            flash(error)
    return render_template("admin/edit_prod.html", name=name, category=category, brand=brand, price=price,
                           description=description)

@bp.route('/products/delete/<p_id>')
@login_required
def del_prod(p_id):
    db = get_db()
    product_id = p_id
    db.execute_sql(
        "DELETE FROM products WHERE id = ?", (product_id,)).fetchone()

    return redirect(url_for('admin.shop'))

@bp.route('users')
@login_required
def users():
    db = get_db()
    users_entries = db.execute_sql(
        "SELECT id, username, firstn, lastn, orders, adresses, email FROM users").fetchall()
    return render_template("admin/users.html", users=users_entries)
