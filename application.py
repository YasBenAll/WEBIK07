from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from flask_uploads import UploadSet, configure_uploads, IMAGES

from helpers import *

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
db = SQL("sqlite:///likestack.db")


@app.route("/")
@login_required
def index():
    """Give dashboard of user."""
    return render_template("index.html")


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

        elif not request.form.get("question"):
            return apology("please answer the security question")

        # encrypt password
        hash = pwd_context.hash(request.form.get("password"))

        # inserting the user into the database
        result = db.execute("INSERT INTO users (username, hash, question) VALUES(:username, :hash, :question)", username=request.form.get("username"), hash=hash, question=request.form.get("question"))

        # check if the username already exists
        if not result:
            return apology("Username already exists", 400)

        print(result)

        # remember which user has logged in
        session["user_id"] = result

        return redirect(url_for("index"))

    else:
        return render_template("register.html")



@app.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    """feed van de gebruiker"""
    if request.method == "GET":



        db.execute()

        return render_template("feed.html")

    else:
        return redirect(url_for("index"))

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    # declare photos as an image uploadset
    photos = UploadSet('photos', IMAGES)

    # declare folder where photos will be upload to
    app.config['UPLOADED_PHOTOS_DEST'] = 'pictures'
    configure_uploads(app, photos)

    if request.method == 'POST' and 'photo' in request.files:
        filename= photos.save(request.files['photo'])
        description = request.form.get("description")
        if not description:
            description = ""
        theme_id = 0
        upload_photo(filename, description, theme_id)

    return render_template('upload.html')

@app.route("/mijn_fotos", methods=["GET", "POST"])
@login_required
def mijn_fotos():
    data = db.execute("SELECT filename FROM pictures WHERE user_id = :user_id", user_id = session["user_id"])
    for item in data:
        print(item)
    return render_template("mijn_fotos.html")