from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory, g
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from flask_uploads import UploadSet, configure_uploads, IMAGES
import urllib,json
import os

MEDIA_FOLDER = os.path.join(os.getcwd(), 'pictures')

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
    return redirect(url_for("feed"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log user in.
    """

    # forget any user_id
    session.clear()

    if request.method == "POST":
        # ensure user input is correct
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("feed"))

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

        ingevoerd_wachtwoord = request.form.get("password")

        if not (any(x.isupper() for x in ingevoerd_wachtwoord) and any(x.islower() for x in ingevoerd_wachtwoord) and any(x.isdigit() for x in ingevoerd_wachtwoord) and len(ingevoerd_wachtwoord) >= 8):
            return apology("please check the password syntax")

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

        return redirect(url_for("uitleg"))

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

        ingevoerd_wachtwoord = request.form.get("password")

        if not (any(x.isupper() for x in ingevoerd_wachtwoord) and any(x.islower() for x in ingevoerd_wachtwoord) and any(x.isdigit() for x in ingevoerd_wachtwoord) and len(ingevoerd_wachtwoord) >= 8):
            return apology("please check the password syntax")

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
    if request.method == "GET":
        if feedgenerator(friends = False) == False:
            return apology("je bent door de stack heen")

        print(session["filename"])
        print("dit is feed")
        return render_template("feed.html", picture=session["filename"], description=session["description"], user_id=session["username_picture"])

    if request.method == "POST":
        marked = 0
        if request.json == 'like':
            marked = 1
        if request.json == 'dislike':
            marked = 2
        if request.json == 'ongepast':
            marked = 3
        if request.json == 'volg':
            followdb = db.execute("SELECT following from users WHERE id=:id", id=session["user_id"])
            picturedb = db.execute("SELECT user_id from pictures WHERE id=:id", id=session["picture_user_id"])
            followlist = json.loads(followdb[0]["following"])
            if picturedb[0]["user_id"] not in followlist:
                followlist.append(session["picture_user_id"])
            followjson = json.dumps(followlist)
            db.execute("UPDATE users SET following = :following WHERE id=:id", following = followjson, id=session["user_id"])

        # update seen_list in database
        seendb = db.execute("SELECT seen_list from users WHERE id=:id", id=session["user_id"])
        seenlist = json.loads(seendb[0]["seen_list"])
        seen_set = set(seenlist)
        seen_set.add(session["photo_id"])
        seen_list = list(seen_set)
        seenjson = json.dumps(seen_list)
        db.execute("UPDATE users SET seen_list = :seen_list WHERE id=:id", seen_list = seenjson, id=session["user_id"])

        db.execute("INSERT INTO history (user_id, photo_id, marked) VALUES(:user_id, :photo_id, :marked)",
                   user_id=session["user_id"], photo_id=session["photo_id"], marked=marked)
        return "saved"

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    urldata = []

    # declare photos as an image uploadset
    photos = UploadSet('photos', IMAGES)

    # declare folder where photos will be uploaded to
    app.config['UPLOADED_PHOTOS_DEST'] = 'pictures'
    configure_uploads(app, photos)

    if request.method == 'POST':

        # upload een foto of gif met beschrijving naar de site
        if 'photo' in request.files:
            print("if photo in request.files")
            filename= photos.save(request.files['photo'])
            description = request.form.get("description")
            if not description:
                description = ""
            theme_id = 0
            upload_photo(filename, description, theme_id)
            return redirect(url_for("feed"))
        if request.form.get("giphy") and not 'photo' in request.files:
            print("request.form.get(giphy)")
            session["giphdescription"] = request.form.get("description")
            keyword = request.form.get("giphy")
            # Download the file from `url` and save it locally under `file_name`:
            data = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/search?q=" + keyword +"&api_key=inu8Jx5h7HWgFC2qHVrS4IzzCZOvVRvr&limit=5").read())
            url = data["data"][0]['images']['downsized']['url']
            urldata = [data["data"][i]['images']['downsized']['url'] for i in range(5)]
            return render_template('upload.html', urldata = urldata, url = url)
        try:
            if request.json['id'] == "send_giphy":
                print("if request.json[id] == send giphy")
                url = request.json['name']
                filename = url.replace("https://","").replace("/","")
                directory = "pictures/" + filename
                urllib.request.urlretrieve(url, directory)
                description = session["giphdescription"]
                if not description:
                    description = ""
                theme_id = 0
                upload_photo(filename, description, theme_id)
                print("uploaded!")
                return redirect(url_for("upload"))
        except:
            return apology("Input keyword")

    else:
        print("else render_template")
        return render_template('upload.html')

@app.route("/friend", methods=["GET", "POST"])
@login_required
def friend():
    # add someone to user's followlist

    followdb = db.execute("SELECT following from users WHERE id=:id", id=session["user_id"])
    followlist = json.loads(followdb[0]["following"])
    for item in followlist:
        follower = db.execute("SELECT username from users WHERE id=:id", id=item)
        for item in follower:
            friend = item["username"]

    return render_template('friend.html', follower = follower, friend=friend)

@app.route("/uitleg", methods=["GET", "POST"])
@login_required
def uitleg():
    return render_template('uitleg.html')

@app.route("/mijn_fotos", methods=["GET", "POST"])
@login_required
def mijn_fotos():
    filenames = dict()
    data = db.execute("SELECT filename FROM pictures WHERE user_id = :user_id", user_id = session["user_id"])
    for item in data:
        print(item["filename"])
    return render_template("mijn_fotos.html", data = data)

@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory(MEDIA_FOLDER, filename, as_attachment=True)

@app.route('/background_process')
def background_process(user_id):
    followdb = db.execute("SELECT following from users WHERE id=:id", id=session["user_id"])
    followlist = json.loads(followdb[0]["following"])
    followlist.append(user_id)
    followjson = json.dumps(followlist)
    db.execute("UPDATE users SET following = :following WHERE id=:id", following = followjson, id=session["user_id"])
    return True

@app.route("/likelist", methods=["GET", "POST"])
@login_required
def likelist():
    datas = db.execute("SELECT photo_id, marked FROM history WHERE user_id = :user_id", user_id = session["user_id"])
    likelist = list()
    for item in datas:
        if item["marked"] == 1:
            liked_foto = db.execute("SELECT filename FROM pictures WHERE id = :photo_id", photo_id = item["photo_id"])
            likelist.append(liked_foto[0]['filename'])
    return render_template("likelist.html", likelist = likelist)

@app.route("/feedcontent", methods=["GET", "POST"])
@login_required
def feedcontent():
    """feed van de gebruiker"""

    if feedgenerator(friends = False) == False:
        return render_template("apologyfeed.html")

    print(session["filename"])
    print("dit is feedcontent")
    return render_template("feedcontent.html", picture=session["filename"], description=session["description"], user_id=session["username_picture"])

@app.route("/apologyfeed")
@login_required
def apologyfeed():
    return apology("je bent door de stack heen")

@app.route("/friendfeed", methods=["GET", "POST"])
@login_required
def friendfeed():

    if request.method == "GET":
        if feedgenerator(friends = True) == False:
            return apology("je bent door de friendstack heen of volgt geen vrienden")

        print(session["filename"])
        print("dit is friendfeed")
        return render_template("friendfeed.html", picture=session["filename"], description=session["description"], user_id=session["username_picture"])

@app.route("/friendfeedcontent", methods=["GET", "POST"])
@login_required
def friendfeedcontent():
    """feed van de gebruiker"""

    if feedgenerator(friends = True) == False:
        return render_template("apologyfeed.html")

    print(session["filename"])
    print("dit is friendfeedcontent")
    return render_template("feedcontent.html", picture=session["filename"], description=session["description"], user_id=session["username_picture"])
