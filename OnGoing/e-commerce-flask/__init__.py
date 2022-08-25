from flask import Flask, blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='dev', )

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import shop
    app.register_blueprint(shop.bp)
    app.add_url_rule("/", endpoint="index")

    from . import cart
    app.register_blueprint(cart.bp)

    # from . import testing
    # app.register_blueprint(testing.bp)

    return app


if __name__ == '__main__':
    create_app()
