import os
import webbrowser
import smtplib
import locale as loc
import re

from flask import Flask, render_template, request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from models import *

# Configure the links for the navigation bar
links = {"Home":"/","Menu":"menu","Register":"register","Log In": "login","Free Pizza!":"xd"}
loglinks = {"Home":"/","Menu":"order","Shopping Cart":"shop","Log Out":"logout","Free Pizza!":"xd"}
loggedin = False

# Configure locale module
loc.setlocale(loc.LC_ALL, 'en_US')

# Configure Flask app
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

# Configure login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configure database
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure session, use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure migrations
Migrate(app, db)

# Configure admin interface
admin = Admin(app, name='Pinocchio Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Pizza, db.session))
admin.add_view(ModelView(Topping, db.session))
admin.add_view(ModelView(Sub, db.session))
admin.add_view(ModelView(SteakTopping, db.session))
admin.add_view(ModelView(Extra, db.session))
admin.add_view(ModelView(DinnerPlatter, db.session))
admin.add_view(ModelView(PlacedOrder, db.session))


# Menu and Ordermenu initialization, 
# takes relevant database data and 
# calculates the new prices based on the give price_per_topping
# Also takes an 'order' argument to create the order dataset
def render_menu(order=True):
    menudict = {}
    if order:
        headers = [" (No topping)", " (1 topping)"," (2 topping)"," (3 topping)", " (special)"]
    else:
        headers = ['']
    templist = []
    queried = Pizza.query.all()
    for pizza in queried:
        for header in range(len(headers)):
            small = float(pizza.small_price_per_topping.split(',')[header])
            large = float(pizza.large_price_per_topping.split(',')[header])
            templist.append({(pizza.pizza_name + headers[header]):[loc.currency((pizza.small_price+small)),loc.currency((pizza.large_price+large))]})
    menudict["Pizza"] = templist
    menudict["Topping"] = [{topping.topping_name:[]} for topping in Topping.query.all()]
    menudict["Sub"] = [{sub.sub_name:[loc.currency(sub.small_price),loc.currency(sub.large_price)]} for sub in Sub.query.all()]
    menudict["Steak Topping"] = [{steaktopping.steak_topping_name:[]} for steaktopping in SteakTopping.query.all()]
    menudict["Extras"] = [{extra.extra_name:[loc.currency(extra.price)]} for extra in Extra.query.all()]
    menudict["Dinner Platters"] = [{dp.dinner_platter_name:[loc.currency(dp.small_price),loc.currency(dp.large_price)]} for dp in DinnerPlatter.query.all()]
    
    return menudict

# Initializes database
def main():
    db.create_all()
    db.session.commit()

# Route for Home
@app.route("/")
def index():
    global loggedin
    if current_user.is_authenticated:
        loggedin = current_user.username
        message = ''
    else:
        message = 'Register or login to make an order!'
    return render_template("home.html", links=links, loglinks=loglinks, loggedin=loggedin, message=message)

# Route for Free Pizza! 
# Opens Pizza-Time youtube video! (Great channel btw)
@app.route("/xd")
def xd():
    global loggedin
    if current_user.is_authenticated:
        loggedin = current_user.username
    webbrowser.open('https://www.youtube.com/watch?v=lpvT-Fciu-4')
    message = "Pizza Time!"
    return render_template("suc.html", links=links, loglinks=loglinks, message=message, loggedin=loggedin)

# Route for Login
# Queries user in database and logs user in if credentials are valid
# Users also end up on this page if they try to go @login_required pages without being logged in
@app.route('/login', methods=['GET', 'POST'])
def login():
    global loggedin
    if loggedin != False:
        return render_template("home.html", links=links, loglinks=loglinks, loggedin=loggedin)
    message = ''
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username, password=password).first()
   
    if user != None:
        login_user(user)
        loggedin = current_user.username
        message = 'Welcome, ' + username
        return render_template('suc.html', links=links, loglinks=loglinks, message=message, loggedin=loggedin)

    if request.method == 'POST':
        message = 'Login with valid credentials'
    return render_template("login.html", links=links, loglinks=loglinks, loggedin=loggedin, message=message)

# Route for Logout
# Logs a user out, not much more to say
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    global loggedin
    logout_user()
    loggedin = False
    message = 'You have been logged out'
    return render_template('suc.html', links=links, loglinks=loglinks, message=message, loggedin=loggedin)

# Route for Register
# Registers the user
@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    message = ''

    # Checks if input is not empty, valid and not taken
    if None not in [username,password, first_name, last_name, email] and '' not in [username,password, first_name, last_name, email]:
        regex ='^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if(re.search(regex,email)): 
            if User.query.filter_by(username=username).first() == None and User.query.filter_by(email=email).first() == None:
                user = User(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
                db.session.add(user)
                db.session.commit()
                message = 'You have been registered, login above.'
                return render_template('login.html', links=links, loglinks=loglinks, message=message, loggedin=loggedin)
            else:
                message = 'Username or E-mail already taken'
        else:
            message = 'E-mail is invalid'
    else:
        message = 'Fill in all fields'

    return render_template('register.html', links=links, loglinks=loglinks, loggedin=loggedin, message=message)

# Route to Menu
# Loads the menu which is defined in an earlier function
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    global loggedin
    if current_user.is_authenticated:
        loggedin = current_user.username
        message = ''
        menudict = render_menu(order=True)
        return render_template('order.html', links=links, loglinks=loglinks, loggedin=loggedin, menudict=menudict, message=message)
    menudict = render_menu()
    return render_template('menu.html', links=links, loglinks=loglinks, loggedin=loggedin, menudict=menudict)

# Route to Order
# Loads all data in and from the database to keep track of the orders
# Here we go...
@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    global loggedin
    if current_user.is_authenticated:
        loggedin = current_user.username

    # Load menu's
    message = ''
    menudict = render_menu()
    orderdict = render_menu(order=False)

    # Load or create order for user
    order = Order.query.filter_by(users_id=current_user.id).first()
    if order == None:
        order = Order(users_id=current_user.id,final=0)
        db.session.add(order)
        db.session.commit()

    # If user adds an item
    if request.method == 'POST':

        # If the item is a pizza load all selected data and calculate price (Special pizza is found here!)
        if request.form.get('Pizza') != None:
            queried = Pizza.query.all()
            pizza = [request.form.get('Pizza').split(';')[0],request.form.get('Pizza').split(';')[1],request.form.get('top0'),request.form.get('top1'),request.form.get('top2')]
            special = request.form.get('special')
            if special != None:
                num_top = 1
            else:
                num_top = 3 - pizza.count('No topping')
        
            # Different price for small and large
            for piz in queried:
                if pizza[0] == piz.pizza_name:
                    if pizza[1] == "small":
                        baseprice = piz.small_price
                        if special != None:
                            fullprice = baseprice + float(piz.small_price_per_topping.split(',')[4])
                        else:
                            fullprice = baseprice + float(piz.small_price_per_topping.split(',')[num_top])
                    if pizza[1] == "large":
                        baseprice = piz.large_price
                        if special != None:
                            fullprice = baseprice + float(piz.large_price_per_topping.split(',')[4])
                        else:
                            fullprice = baseprice + float(piz.large_price_per_topping.split(',')[num_top])
            fullprice = loc.currency(fullprice)

            pizza.append(fullprice)
            message = '1x ' + pizza[1] + ' ' + pizza[0] + ' with ' + str(num_top) + ' topping(s) has been added to the'
            
            # Format toppings
            topping = []
            for x in pizza[2:5]:
                if x == 'No topping':
                    topping.append('')
                else:
                    topping.append(x)
            topping = str(topping[0] + ', ' + topping[1] + ', ' + topping[2])
            if topping == ', , ':
                topping = None
            if special != None:
                topping = 'Imported Wuhan-style medium-rare bat'
            
            # Add pizza to order
            order.add_item(pizza[0],pizza[1],topping,pizza[5])

        # If the item is a sub
        if request.form.get('Sub') != None:
            queried = Sub.query.all()
            sub = [request.form.get('Sub').split(';')[0],request.form.get('Sub').split(';')[1],request.form.get('cheese')]
            steak = request.form.get('top')
            if steak == None:
                sub.append('No topping')
            else:
                sub.append(steak)
            
            # Cheese and Steak topping cost 50 cent extra. What a steal!
            cheese = sub[2]
            add = 0
            steak_top = ''
            if cheese == "Cheese":
                add += 0.5
            if sub[3] != "No topping":
                add += 0.5
                steak_top = ' with 1 topping'
            
            # Different price for small and large
            for s in queried:
                if sub[0] == s.sub_name:
                    if sub[1] == "small":
                        baseprice = s.small_price
                    if sub[1] == "large":
                        baseprice = s.large_price
            fullprice = loc.currency(baseprice+add)

            sub.append(fullprice)
            message = '1x ' + sub[1] + ' ' + sub[0] + steak_top + ' has been added to the'
            
            # Format toppings
            topping = []
            for x in sub[2:4]:
                if x == 'No topping':
                    topping.append('')
                else:
                    topping.append(x)
            if topping[1] == '':
                topping = str(topping[0] + topping[1])
            else:
                topping = str(topping[0] + ', ' + topping[1])
            if topping == ', ':
                topping = None

            # Add sub to order
            order.add_item(sub[0],sub[1],topping,sub[4])

        # If the item is an extra
        if request.form.get('Extras') != None:
            queried = Extra.query.all()
            ex = [request.form.get('Extras')]

            for extr in queried:
                if ex[0] == extr.extra_name:
                    baseprice = extr.price
            fullprice = loc.currency(baseprice)

            ex.append(fullprice)
            message = '1x ' + ex[0] + ' has been added to the'
            print(ex)

            # Add extra to order
            order.add_item(ex[0],size='',toppings=None,money=ex[1])

        # If the item is a dinner platter
        if request.form.get('Dinner') != None:
            print('xd')
            queried = DinnerPlatter.query.all()
            dp = [request.form.get('Dinner').split(';')[0],request.form.get('Dinner').split(';')[1]]
            for d in queried:
                if dp[0] == d.dinner_platter_name:
                    if dp[1] == "small":
                        baseprice = d.small_price
                    if dp[1] == "large":
                        baseprice = d.large_price
            fullprice = loc.currency(baseprice)

            dp.append(fullprice)
            message = '1x ' + dp[1] + ' ' + dp[0] + ' has been added to the'
            
            # Add Dinner platter to order
            order.add_item(dp[0],size=dp[1],toppings=None,money=dp[2])


    return render_template('order.html', links=links, loglinks=loglinks, loggedin=loggedin, menudict=menudict, orderdict=orderdict, message=message)

# Route to Shop
# Loads all cart items and arranges them in a table
# Also sends an Email confirmation to the user
@app.route('/shop', methods=['GET', 'POST'])
@login_required
def shop():
    global loggedin
    if current_user.is_authenticated:
        loggedin = current_user.username

    # Creates order if there is none, otherwise it loads the order
    order = Order.query.filter_by(users_id=current_user.id).first()
    if order == None:
        order = Order(users_id=current_user.id,final=0)
        db.session.add(order)
        db.session.commit()
    items = Item.query.filter_by(order_id=order.id).all()

    # Count the Mula/Cash/Money/Knaken/Doekoe/Dinero/Stacks/Flappen $$$
    count = 0
    for item in items:
        count += float(item.money.replace('$',''))
    total = loc.currency(count)

    if request.method == "POST":

        # Clear the cart
        if request.form.get('clear') != None:
            for item in items:
                db.session.delete(item)
                db.session.commit()
            db.session.delete(order)
            db.session.commit()
            message = 'Shopping cart cleared.'
            return render_template('suc.html', links=links, loglinks=loglinks, loggedin=loggedin, message=message)
        
        # Send a confirmation E-mail
        if request.form.get('send') != None:
            placed = PlacedOrder(users_id=current_user.id,username=loggedin,total=order.final,items=len(items))
            db.session.add(placed)
            db.session.commit()
            
            send_to_email = current_user.email
            email = os.getenv("EMAIL_USER")
            password = os.getenv("EMAIL_PASS")
            subject = 'Your Pizza order'
            messagePlain = 'Dear ' + loggedin + ',\n' + 'Your pizza order has been recieved and is being prepared.\nYou ordered:\n'
            messageHTML = '<h3>Dear ' + loggedin + ',</h3><br>' + '<p>Your pizza order has been recieved and is being prepared.<br>You ordered:<br></p>'
            
            # Create the table
            table = '<table><thead><tr><th>Dish</th><th>Size</th><th>Price</th><th>Toppings</th><th>Total</th></tr></thead><tbody>'
            for item in items:
                table = table + '<tr><td>' + item.item_name + ' </td>'
                table = table + '<td>' + item.size + ' </td>'
                table = table + '<td>' + item.money + ' </td>'
                if item.toppings == None:
                    table = table + '<td></td>'
                else:
                    table = table + '<td>' + item.toppings + '</td></tr>'
            table = table + '<tr><td></td><td></td><td></td><td></td><td>' + total + '</td></tr></tbody></table>'
            messageHTML = messageHTML +table

            msg = MIMEMultipart('alternative')
            msg['From'] = email
            msg['To'] = send_to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(messagePlain, 'plain'))
            msg.attach(MIMEText(messageHTML, 'html'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, send_to_email, text)
            server.quit()
            message = 'Your order has been placed and a confirmation email has been sent!'

            # Clear the cart
            for item in items:
                db.session.delete(item)
                db.session.commit()
            db.session.delete(order)
            db.session.commit()
            
            return render_template('suc.html', links=links, loglinks=loglinks, loggedin=loggedin, message=message)
    
    # Add total to order
    order.final = total
    db.session.commit()

    return render_template('shop.html', links=links, loglinks=loglinks, loggedin=loggedin, items=items, total=total)

if __name__ == "__main__":
    with app.app_context():
        main()