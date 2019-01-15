from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *
from upload import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Give dashboard of user."""
    return render_template("index.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")

        if not request.form.get("shares"):
            return apology("must provide amount")

        # check if the given number is an integer
        try:
            if int(request.form.get("shares")) < 0:
                return apology("number must be greater than 0")
        except:
            return apology("number must be an integer")

        aandeel = lookup(request.form.get("symbol"))

        if aandeel == None:
            return apology("symbol does not exist")

        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        # check if the user has enough cash to buy the stock(s)
        if float(cash[0]["cash"]) - (int(request.form.get("shares"))*float(aandeel["price"])) < 0.0:
            return apology("not enough money")

        number = int(request.form.get("shares"))
        price = number*aandeel["price"]

        # make a new row into the table sales
        db.execute("INSERT INTO sales (username, stock, amount, price) VALUES(:id, :symbol, :number, :price)",
                   symbol=aandeel["symbol"], number=number, price=usd(price), id=session["user_id"])

        # subtract the price from user's cash
        db.execute("UPDATE users SET cash = cash - :price WHERE id = :id", id=session["user_id"], price=price)

        return redirect(url_for("index"))


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    # select all the data we need from sales
    history = db.execute("SELECT stock, amount, time, price FROM sales WHERE username = :user_id ", user_id=session["user_id"])

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide stock symbol")

        # lookup the data for the symbol
        aandeel = lookup(request.form.get("symbol"))

        # check if the symbol exists in the database
        if aandeel == None:
            return apology("symbol does not exist")

        return render_template("quoted.html", data=aandeel)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username")

        elif not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("confirmation"):
            return apology("must provide password")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must be the same")

        # insert the new user in the database
        user = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                          username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))

        print(user)

        # check if the username already exists
        if not user:
            return apology("username already exists", 400)

        # remember which user has logged in
        session["user_id"] = user

        return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    if request.method == "POST":

        if not request.form.get("shares"):
            return apology("must provide amount")

        # select the given symbol and with the total amount of stocks the user has of that symbol
        data = db.execute("SELECT stock, SUM(amount) as total_amount FROM sales WHERE username = :user_id and stock = :aandeel GROUP BY stock HAVING total_amount > 0",
                          user_id=session["user_id"], aandeel=request.form.get("symbol"))

        # check if the user can sell his shares
        if int(request.form.get("shares")) > data[0]["total_amount"]:
            return apology("you do not have enough shares")

        # lookup the current stock price
        aandeel = lookup(request.form.get("symbol"))

        number = -int(request.form.get("shares"))

        # calculate how much the users owes
        sell = (aandeel["price"])*(int(request.form.get("shares")))

        # add cash to the user's cash
        db.execute("UPDATE users SET cash = cash + :price WHERE id = :id", id=session["user_id"], price=sell)

        # add the sell to the database
        db.execute("INSERT INTO sales (username, stock, amount, price) VALUES(:id, :symbol, :number, :price)",
                   symbol=aandeel["symbol"], number=number, price=usd(sell), id=session["user_id"])

        return redirect(url_for("index"))

    if request.method == "GET":

        # select which stocks the user has
        data = db.execute(
            "SELECT stock, SUM(amount) as total_amount FROM sales WHERE username = :user_id GROUP BY stock HAVING total_amount > 0", user_id=session["user_id"])

        return render_template("sell.html", data=data)


@app.route("/top_up", methods=["GET", "POST"])
@login_required
def top_up():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("top_up.html")

    if request.method == "POST":

        if not request.form.get("cash"):
            return apology("must provide cash")

        money = request.form.get("cash")

        # update the users's cash
        db.execute("UPDATE users SET cash = cash + :money WHERE id = :id", id=session["user_id"], money=money)

        return redirect(url_for("index"))

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        upload()
