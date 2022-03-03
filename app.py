import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
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
    Returns the home page.
    """
    return render_template("home.html", page_title="Home")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    GET: Returns the login page.
    POST: Collects submitted user credentials.
    If username and passsword are correct, user is logged in and 
    redirected to the home page.
    If username and password are incorrect, user is redirected to
    the login page.
    """
    if request.method == "POST":
        username = request.form.get("username").lower()
        valid_username = mongo.db.users.find_one({"username": username})

        if valid_username:
            if check_password_hash(
                    valid_username["password"], request.form.get("password")):
                session["user"] = username
                flash(f"Welcome, {username}")
                return redirect(url_for('home'))

            flash("Username or password incorrect. Please try again.")
            return redirect(url_for('login'))

        flash("Username or password incorrect. Please try again.")
        return redirect(url_for('login'))

    return render_template("login.html", page_title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    GET: Returns the registration page.
    POST: Collects submitted user data and checks if requested username is 
    available.
    If username is taken, user is returned to the registration page.
    If username is available, a new user record is added to the users database
    and the user is logged in and redirected to the home page.
    """
    if request.method == "POST":
        # Assign submitted username to a variable and check if it exists in 
        # the database
        username = request.form.get("username").lower()
        duplicate_user = mongo.db.users.find_one({"username": username})

        # If username already exists, return user to registration page
        if duplicate_user:
            flash(f"Username \"{username}\" is unavailable.")
            return redirect(url_for("register"))

        new_user = {
            "username": username,
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password"))
        }

        mongo.db.users.insert_one(new_user)

        session["user"] = username
        flash(f"Welcome, {session['user']}! Your account has been created.")
        return redirect(url_for('home'))
    return render_template("register.html", page_title="Register")


@app.route('/logout')
def logout():
    """
    Removes the user from the session cookie.
    Returns a redirect to the home page.
    """
    session.pop("user")
    flash("You have been logged out.")
    return redirect(url_for('home'))


@app.route('/workout_log')
def workout_log():
    """
    Finds all workouts logged by the user and returns the workout log page. 
    """
    # find all workouts logged by the current user
    # lookup corresponding routine details using routine_id
    logs = list(mongo.db.workout_logs.aggregate([
        {
            "$match": {
                "username": session['user']
            }
        },
        {
            "$lookup": {
                "from": "routines",
                "localField": "routine_id",
                "foreignField": "_id",
                "as": "routine"
            }
        },
        {
            "$sort": {
                "date": -1
            }
        }
        ]))
    return render_template('workout_log.html', page_title="Workout Log", logs=logs)


@app.route("/add_workout", methods=["GET", "POST"])
def add_workout():
    """
    GET: returns the Add Workout page
    POST: collects user input, inserts to workout_logs database and
    redirects user to Workout Log page
    """
    if request.method == "POST":
        # concatenate date picker value and time picker value
        date = request.form.get("workout_date") + request.form.get("workout_time")
        # convert concatenated date into ISODate 
        iso_date = datetime.datetime.strptime(date, "%d %B %y%I:%M %p")
        # build dictionary containing workout details
        entry = {
            "routine_id": ObjectId(request.form.get("routine_name")),
            "date": iso_date,
            "notes": request.form.get("notes"),
            "sets": int(request.form.get("sets")),
            "username": session['user']
        }
        # insert dictionary into database
        mongo.db.workout_logs.insert_one(entry)
        
        flash("Workout record added!")
        return redirect(url_for("workout_log"))

    # find default routines (created by admin)
    default_routines = list(mongo.db.routines.find({"username": "admin"}))
    # find user's custom routines
    user_routines = list(mongo.db.routines.find({"username": session['user']}))
    # concatenate default and custom routines
    routines = default_routines + user_routines
    return render_template(
        "add_workout.html", page_title="Add Workout", routines=routines)


@app.route("/edit_workout/<log_id>", methods=["GET", "POST"])
def edit_workout(log_id):
    """
    GET: Returns edit_workout page with data from requested log id
    POST: If current user created the log entry, updates the entry.
    Otherwise, returns user to workout log page.
    """
    if request.method == "POST":
        # find log entry to edit from database
        log = mongo.db.workout_logs.find_one({"_id": ObjectId(log_id)})
        # check current user is the user who created the entry
        if log["username"] == session["user"]:
            # concatenate date picker value and time picker value
            date = request.form.get("workout_date") + request.form.get("workout_time")
            # convert concatenated date into ISODate
            iso_date = datetime.datetime.strptime(date, "%d %B %y%I:%M %p")
            # build dictionary containing workout details
            entry = {
                "routine_id": ObjectId(request.form.get("routine_name")),
                "date": iso_date,
                "notes": request.form.get("notes"),
                "sets": int(request.form.get("sets")),
                "username": session['user']
            }
            flash("Workout record updated.")
            # update the database entry with the entered details
            mongo.db.workout_logs.update_one(log, {"$set": entry})
            return redirect(url_for("workout_log"))

        # redirect unauthorised users to workout log page
        flash("You don't have permission to edit this log.")
        return redirect(url_for("workout_log"))

    # find log entry to edit from database
    log = mongo.db.workout_logs.find_one({"_id": ObjectId(log_id)})
    # find default routines (created by admin)
    default_routines = list(mongo.db.routines.find({"username": "admin"}))
    # find user's custom routines
    user_routines = list(mongo.db.routines.find({"username": session['user']}))
    # concatenate default and custom routines
    routines = default_routines + user_routines
    return render_template(
        "edit_workout.html", page_title="Edit Workout",
        log=log, routines=routines)


@app.route("/delete_workout/<log_id>")
def delete_workout(log_id):
    """
    Checks if current user created the log entry to be deleted
    and deletes it if so.
    Otherwise, returns user to workout log page.
    """
    # find log entry to edit from database
    log = mongo.db.workout_logs.find_one({"_id": ObjectId(log_id)})
    # check current user is the user who created the entry
    if log["username"] == session["user"]:
        mongo.db.workout_logs.delete_one(log)
        flash("Workout record deleted.")
        return redirect(url_for("workout_log"))
    # redirect unauthorised users to workout log page
    flash("You don't have permission to delete this log.")
    return redirect(url_for("workout_log"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
