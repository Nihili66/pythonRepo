from flask import Flask, render_template
from apps/e-commerce-flask/__init__ import app as shop

app = Flask(__name__)


@app.route('/')
def desktop():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
