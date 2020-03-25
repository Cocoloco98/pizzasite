from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# We create all classes needed for the database
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)

class Pizza(db.Model):
    __tablename__ = 'pizza'
    id = db.Column(db.Integer, primary_key=True)
    pizza_name = db.Column(db.String(128), nullable=False)
    small_price = db.Column(db.Float())
    large_price = db.Column(db.Float())
    small_price_per_topping = db.Column(db.String(128))
    large_price_per_topping = db.Column(db.String(128))

class Topping(db.Model):
    __tablename__ = 'topping'
    id = db.Column(db.Integer, primary_key=True)
    topping_name = db.Column(db.String(128), nullable=False)

class Sub(db.Model):
    __tablename__ = 'sub'
    id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String(128), nullable=False)
    small_price = db.Column(db.Float())
    large_price = db.Column(db.Float())

class SteakTopping(db.Model):
    __tablename__ = 'steaktopping'
    id = db.Column(db.Integer, primary_key=True)
    steak_topping_name = db.Column(db.String(128), nullable=False)

class Extra(db.Model):
    __tablename__ = 'extra'
    id = db.Column(db.Integer, primary_key=True)
    extra_name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float(), nullable=False)

class DinnerPlatter(db.Model):
    __tablename__ = 'dinnerplatters'
    id = db.Column(db.Integer, primary_key=True)
    dinner_platter_name = db.Column(db.String(128), nullable=False)
    small_price = db.Column(db.Float(), nullable=False)
    large_price = db.Column(db.Float(), nullable=False)

# Order has a function which adds items to an order
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    final = db.Column(db.String(128), nullable=False)

    def add_item(self,name,size,toppings,money):
      item = Item(item_name=name, size=size, toppings=toppings, money=money,order_id=self.id)
      db.session.add(item)
      db.session.commit()

class PlacedOrder(db.Model):
    __tablename__ = 'placedorder'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    username = db.Column(db.String(128))
    total = db.Column(db.String(128), nullable=False)
    items = db.Column(db.Integer, nullable=False)

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(128), nullable=False)
    size = db.Column(db.String(128))
    toppings = db.Column(db.String(128))
    money = db.Column(db.String(128), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))