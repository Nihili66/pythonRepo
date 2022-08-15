from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='dev', )

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import budget
    app.register_blueprint(budget.bp)
    app.add_url_rule("/", endpoint="index")

    # from . import testing
    # app.register_blueprint(testing.bp)

    return app


if __name__ == '__main__':
    create_app()
