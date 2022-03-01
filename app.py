import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    """
    Returns the home page for users who aren't logged in.
    """
    return render_template("home.html", page_title="Home")


@app.route("/login")
def login():
    """
    Returns the login page.
    """
    return render_template("login.html", page_title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Returns the registration page.
    """
    if request.method == "POST":
        # Assign the submitted username to a variable and check if it exists in the database
        username = request.form.get("username").lower()
        duplicate_user = mongo.db.users.find_one({"username": username})

        # If username already exists, return user to registration page 
        if duplicate_user:
            flash(f"Username \"{username}\" is unavailable.")
            return redirect(url_for("register"))

        new_user = {
            "username": username,
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
        }

        mongo.db.users.insert_one(new_user)

        session["user"] = username
        flash(f"Welcome, {session['user']}! Your account has been created.")
        return redirect(url_for('home'))
    return render_template("register.html", page_title="Register")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
