from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from flask_uploads import UploadSet, configure_uploads, IMAGES

import random

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

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation")

        # check if password and password confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must be the same")

        # ensure answer was submitted
        elif not request.form.get("question"):
            return apology("please answer the security question")

        # encrypt password
        hash = pwd_context.hash(request.form.get("password"))

        # inserting the user into the database
        result = db.execute("INSERT INTO users (username, hash, question) VALUES(:username, :hash, :question)", username=request.form.get("username"), hash=hash, question=request.form.get("question"))

        # error when username already exists
        if not result:
            return apology("Username already exists")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect(url_for("index"))

    else:
        return render_template("register.html")

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    """ change user password """

    session.clear()

    if request.method == 'POST':

        if not request.form.get("username"):
            return apology("must provide username")

        elif not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must be the same")

        elif not request.form.get("question"):
            return apology("please answer the security question")

        # encrypt password
        hash = pwd_context.hash(request.form.get("password"))

        # check if username and security question match
        username = request.form.get("username")
        security_question = request.form.get("question")
        users = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        username_from_database = users[0]["username"]
        security_question_from_database = users[0]["question"]

        if username == username_from_database and security_question == security_question_from_database:

            # update the password
            db.execute("UPDATE users SET hash=:hash WHERE username=:username", hash=hash, username=username_from_database)

            # remember which user has logged in
            session["user_id"] = users[0]["id"]
            return redirect(url_for("index"))

        else:
            return apology("Username and answer don't match")

    else:
        return render_template("forgot.html")

@app.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    """feed van de gebruiker"""

    if request.method == "GET":

        marked = 0
        seen_list = list()

        amount = db.execute("SELECT COUNT(id) FROM pictures")
        history_list = db.execute("SELECT photo_id FROM history WHERE user_id = :user_id", user_id=session["user_id"])

        print(history_list)

        for item in history_list:
            seen_list.append(item['photo_id'])

        print(amount[0]['COUNT(id)'])

        rand = random.randrange(1, int(amount[0]['COUNT(id)'])+1)

        print(rand)

        while rand not in seen_list:
            rand = random.randrange(1, int(amount[0]['COUNT(id)'])+1)

        picture = db.execute("SELECT filename, description FROM pictures WHERE id = :id", id=rand)

        db.execute("INSERT INTO history (user_id, photo_id, marked) VALUES(:user_id, :photo_id, :marked)",
                   user_id=session["user_id"], photo_id=rand, marked=marked)

        return render_template("feed.html", picture="\\pictures\\"+picture[0]['filename'], description=picture[0]['description'])

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


@app.route("/friend", methods=["GET", "POST"])
@login_required
def friend():
    if request.method == 'POST':
        db.execute("UPDATE users SET following = :following + following WHERE id=:id", following = 1, id=session["user_id"])
    return render_template('friend.html')

@app.route("/mijn_fotos", methods=["GET", "POST"])
@login_required
def mijn_fotos():
    data = db.execute("SELECT filename FROM pictures WHERE user_id = :user_id", user_id = session["user_id"])
    for item in data:
        print(item)
    return render_template("mijn_fotos.html")
