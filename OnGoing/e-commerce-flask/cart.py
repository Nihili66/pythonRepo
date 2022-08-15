from flask import Blueprint, render_template, session, redirect, url_for, g, request, flash
from auth import login_required
from db import get_db

bp = Blueprint('cart', __name__, url_prefix='/cart')

class Cart:
    def __init__(self):
        self.total = 0

    def add(self, price):
        self.total += price

@bp.before_app_request
def get_cart():
    db = get_db()
    product_list = session.get('cart')
    g.cart = []
    c = Cart()
    if product_list:
        for product_id in product_list:
            product = db.execute_sql(
                "SELECT name, category, price, id FROM products WHERE id = ?", (product_id,)).fetchone()
            c.add(int(product[2]))
            g.cart.append(product)
    g.carttotal = c.total

@bp.route('/')
def cart():
    return render_template("shop/cart.html", cart_list=g.cart, cart_total=g.carttotal)

@bp.route('/add/<p_id>')
def add_cart(p_id):
    product_id = p_id
    cart_list = session.get('cart')
    if not cart_list:
        session['cart'] = [product_id]
    else:
        cart_list.append(product_id)
        del session['cart']
        session['cart'] = cart_list
    return redirect(url_for('shop.shop'))

@bp.route('/del/<p_id>')
def del_cart(p_id):
    product_id = p_id
    cart_list = session.get('cart')
    if cart_list:
        cart_list.remove(product_id)
        del session['cart']
        session['cart'] = cart_list
    return redirect(url_for('cart.cart'))

@bp.route('/reset')
def reset_cart():
    if session.get('cart'):
        del session['cart']
    return redirect(url_for('cart.cart'))

@bp.route('/checkout', methods=('GET', 'POST'))
@login_required
def checkout():
    if request.method == "POST":
        products = ";".join(session.get('cart'))
        shipping_price = request.form['deliverymethod']
        total_price = int(g.carttotal) + int(shipping_price)
        full_name = request.form['first-name'] + " " + request.form['last-name']
        adress = request.form['address']
        city = request.form['city']
        postal_code = request.form['postal-code']
        country = request.form['country']
        adresse = adress + "; " + city + "; " + postal_code + "; " + country
        phone = request.form['phone']
        error = None

        if not shipping_price:
            error = "Shipping method is required."

        if not error:
            db = get_db()
            db.execute_sql(
                "INSERT INTO orders (user_id, products, shipping, total, full_name, adresse, phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (g.user[0], products, shipping_price, total_price, full_name, adresse, phone),
            )
            if session.get('cart'):
                del session['cart']
            return render_template('shop/order_success.html', cart_list=g.cart, cart_total=g.carttotal, shipping=shipping_price,
                                   total=total_price, adress=adress, city=city, postal_code=postal_code, country=country)
        else:
            flash(error)

    return render_template('shop/checkout.html',  cart_list=g.cart, cart_total=g.carttotal)
