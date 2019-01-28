from cs50 import SQL
import csv
import urllib.request, json
import random

from flask import redirect, render_template, request, session
from functools import wraps
db = SQL("sqlite:///likestack.db")

def apology(message, code=400):
    """Renders message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def upload_photo(filename, description, theme_id):
    # store the picture into the database
    print("uploaded something")
    return db.execute("INSERT INTO pictures(user_id, filename, description, theme_id) VALUES(:user_id, :filename, :description, :theme_id)", user_id = session["user_id"] , filename = filename, description = description, theme_id = theme_id)

def add_friend():
    pass

def giphy():
    data = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/search?q=hamburger&api_key=inu8Jx5h7HWgFC2qHVrS4IzzCZOvVRvr&limit=5").read())
    return data["data"][0]['images']['downsized']['url']

def feedgenerator():

    seendb = db.execute("SELECT seen_list from users WHERE id=:id", id=session["user_id"])
    seenlist = json.loads(seendb[0]["seen_list"])
    print("seendb=", seendb)
    print("seenlist=", seenlist)
    seenset = set(seenlist)
    set_all = set()
    amount = db.execute("SELECT id FROM pictures WHERE NOT :user_id = user_id", user_id = session["user_id"])

    # mijn idee van hoe je alleen foto's van mensen die je volgt kan laten zien. Dit werkt alleen nog niet :'(
    # amount_friends = db.execute("SELECT id FROM pictures WHERE id in friendlist", friendlist = db.execute("SELECT following from users WHERE id=:id", id=session["user_id"])[0]["following"])

    for item in amount:
        set_all.add(item['id'])
    notseen = set()
    notseen = set_all - seenset
    print("notseen= ", notseen)
    if notseen == set():
        return False
    else:
        notseenlist = list(notseen)
        rand = random.choice(notseenlist)
        picture = db.execute("SELECT filename, description, user_id, id FROM pictures WHERE id = :id", id=rand)
        username = db.execute("SELECT username FROM users WHERE id = :id", id=picture[0]['user_id'])
        session["photo_id"] = rand
        session["picture_user_id"] = picture[0]["user_id"]
        session["filename"] = picture[0]['filename']
        session["description"] = picture[0]['description']
        session["username_picture"] = username[0]['username']
        return True
