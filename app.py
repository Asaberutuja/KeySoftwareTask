from flask import Flask, render_template, request, redirect, url_for
from models import db, Category, Attribute, Product, ProductAttributeValue

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Home
@app.route("/")
def index():
    return render_template("base.html")

# Categories
@app.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == "POST":
        name = request.form["name"]
        desc = request.form.get("description", "")
        db.session.add(Category(name=name, description=desc))
        db.session.commit()
        return redirect(url_for("categories"))
    cats = Category.query.all()
    return render_template("categories.html", categories=cats)

# Attributes
@app.route("/attributes", methods=["GET", "POST"])
def attributes():
    if request.method == "POST":
        name = request.form["name"]
        dtype = request.form["dataType"]
        db.session.add(Attribute(name=name, dataType=dtype))
        db.session.commit()
        return redirect(url_for("attributes"))
    attrs = Attribute.query.all()
    return render_template("attributes.html", attributes=attrs)

# Products
@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "POST":
        name = request.form["name"]
        sku = request.form["sku"]
        price = float(request.form["price"])
        categoryId = int(request.form["categoryId"])
        product = Product(name=name, sku=sku, price=price, categoryId=categoryId)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("products"))

    prods = Product.query.all()
    cats = Category.query.all()
    return render_template("products.html", products=prods, categories=cats)

if __name__ == "__main__":
    app.run(debug=True)
