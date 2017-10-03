from flask import Flask
from flask import render_template, abort
# request, url_for, redirect,
#    abort

# import os
from .models import Product
from .db import init_sessionmaker, initial_setup

app = Flask(__name__)

DBSession = init_sessionmaker()


@app.teardown_appcontext
def shutdown_session(exception=None):
    DBSession.remove()


@app.route("/")
def catalog():
    session = DBSession()
    products = session.query(Product).all()
    return render_template("list.html", products=products)


@app.route("/products/<int:product_id>/")
def product_detail(product_id):
    session = DBSession()
    product = session.query(Product).filter_by(id=product_id).first()
    if product is None:
        abort(404)
    return render_template("product.html", product=product)


@app.cli.command()
def init_db():
    initial_setup()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
