from cs50 import SQL
import csv
import urllib.request, json
import random

from flask import redirect, render_template, request, session
from functools import wraps
db = SQL("sqlite:///likestack.db")

def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


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
    return db.execute("INSERT INTO pictures(user_id, filename, description, theme_id) VALUES(:user_id, :filename, :description, :theme_id)", user_id = session["user_id"] , filename = filename, description = description, theme_id = theme_id)

def add_friend():
    pass

def giphy():
    data = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/search?q=hamburger&api_key=inu8Jx5h7HWgFC2qHVrS4IzzCZOvVRvr&limit=5").read())
    return data["data"][0]['images']['downsized']['url']

def feedgenerator():
    seen_list = list()
    amount = db.execute("SELECT id FROM pictures")
    history_list = db.execute("SELECT photo_id FROM history WHERE user_id = :user_id", user_id=session["user_id"])

    for item in history_list:
        seen_list.append(item['photo_id'])

    rand = random.choice(amount)
    # rand = random.randrange(1, int(amount[0]['id'])+1) - Werkt niet aangezien sommige foto's uit de database verwijderd zijn.

    picture = db.execute("SELECT filename, description, user_id, id FROM pictures WHERE id = :id", id=rand['id'])
    username = db.execute("SELECT username FROM users WHERE id = :id", id=picture[0]['user_id'])
    session["photo_id"] = rand['id']
    session["picture_user_id"] = picture[0]["user_id"]

    return picture, username