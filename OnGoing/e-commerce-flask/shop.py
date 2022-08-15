from flask import Blueprint, render_template, session, redirect, url_for
from db import get_db

bp = Blueprint('shop', __name__)

@bp.route('/')
def index():
    return render_template("shop/index.html")

@bp.route('/shop')
def shop():
    db = get_db()
    product_entries = db.execute_sql(
        "SELECT name, price, id FROM products").fetchall()
    return render_template("shop/shop.html", product_entries=product_entries)

@bp.route('/product/<p_id>')
def product_page(p_id):
    db = get_db()
    product_id = p_id
    product = db.execute_sql(
        "SELECT name, category, brand, price, desc FROM products WHERE id = ?", (product_id,)).fetchone()
    name = product[0]
    category = product[1]
    brand = product[2]
    price = product[3]
    description = product[4]
    return render_template("shop/product.html", name=name, category=category, brand=brand, price=price,
                           description=description)
