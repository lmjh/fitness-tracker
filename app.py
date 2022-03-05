import os
import datetime
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


def login_required(f):
    """
    Decorator to check if a user is currently logged in and redirect to the login
    page if not.
    Based on this function from the Flask documetation:
    https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/#login-required-decorator
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            flash("You must login to access this page.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


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
@login_required
def logout():
    """
    Removes the user from the session cookie.
    Returns a redirect to the home page.
    """
    session.pop("user")
    flash("You have been logged out.")
    return redirect(url_for('home'))


@app.route('/workout_log')
@login_required
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
@login_required
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
@login_required
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
@login_required
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


@app.route("/my_routines")
@login_required
def my_routines():
    default_routines = list(mongo.db.routines.find({"username": "admin"}))
    custom_routines = list(mongo.db.routines.find({"username": session["user"]}))
    return render_template("my_routines.html", page_title="My Routines", default_routines=default_routines, custom_routines=custom_routines)


@app.route("/add_routine", methods=["GET", "POST"])
@login_required
def add_routine():
    """
    GET: Render add routing page template
    POST:
    """
    if request.method == "POST":
        # Assign submitted routine name to a variable and check if the current
        # user or admin already has a routine of this name
        routine_name = request.form.get("routine_name")
        duplicate_routine = mongo.db.routines.find_one(
            {
                "$or": [
                    {
                        "username": session["user"],
                        "routine_name": routine_name
                    },
                    {
                        "username": "admin",
                        "routine_name": routine_name
                    }
                ]
            })
        # if a record is found matching user and routine name, redirect
        # to add_routine page
        if duplicate_routine:
            flash("Duplicate routine name. Please enter a unique routine name.")
            return redirect(url_for("add_routine"))

        # build dictionary from user's entered data
        new_routine = {
            "routine_name": routine_name,
            "exercise_one": request.form.get("exercise_one"),
            "exercise_one_reps": request.form.get("exercise_one_reps"),
            "exercise_two": request.form.get("exercise_two"),
            "exercise_two_reps": request.form.get("exercise_two_reps"),
            "exercise_three": request.form.get("exercise_three"),
            "exercise_three_reps": request.form.get("exercise_three_reps"),
            "username": session["user"]
        }
        # insert new routine dictionary to database
        mongo.db.routines.insert_one(new_routine)
        flash("New routine successfully added.")
        return redirect(url_for("my_routines"))

    return render_template("add_routine.html", page_title="Add Routine")


@app.route("/edit_routine/<routine_id>", methods=["GET", "POST"])
@login_required
def edit_routine(routine_id):
    """
    GET: Returns edit_routine page with data from requested routine id
    POST: 
    """
    if request.method == "POST":
        # find routine to edit from database
        routine = mongo.db.routines.find_one({"_id": ObjectId(routine_id)})
        # check current user is the user who created the routine
        if routine["username"] == session["user"]:
            # assign the submitted routine name to a variable
            routine_name = request.form.get("routine_name")
            # check if the submitted routine name has changed
            if routine_name != routine["routine_name"]:
                # check if the current user or admin already has a routine with
                # the requested name
                duplicate_routine = mongo.db.routines.find_one(
                    {
                        "$or": [
                            {
                                "username": session["user"],
                                "routine_name": routine_name
                            },
                            {
                                "username": "admin",
                                "routine_name": routine_name
                            }
                        ]
                    })
                # if a matching routine is found, redirect back to edit
                # routine page
                if duplicate_routine:
                    flash(
                        "Duplicate routine name. Please enter a unique routine"
                        " name.")
                    return redirect(url_for(
                        "edit_routine", routine_id=routine_id))
            # build dictionary containing routine details
            entry = {
                "routine_name": routine_name,
                "exercise_one": request.form.get("exercise_one"),
                "exercise_one_reps": request.form.get("exercise_one_reps"),
                "exercise_two": request.form.get("exercise_two"),
                "exercise_two_reps": request.form.get("exercise_two_reps"),
                "exercise_three": request.form.get("exercise_three"),
                "exercise_three_reps": request.form.get("exercise_three_reps"),
                "username": session["user"]
            }
            flash("Routine updated.")
            # update the database entry with the entered details
            mongo.db.routines.update_one(routine, {"$set": entry})
            return redirect(url_for("my_routines"))

        # redirect unauthorised users to workout log page
        flash("You don't have permission to edit this routine.")
        return redirect(url_for("my_routines"))

    # find routine to edit from database
    routine = mongo.db.routines.find_one({"_id": ObjectId(routine_id)})
    return render_template(
        "edit_routine.html", page_title="Edit Routine", routine=routine)


@app.route("/delete_routine/<routine_id>")
@login_required
def delete_routine(routine_id):
    """
    Deletes the requested routine and all logs using that routine from the
    database, then redirects the user to the my_routines page
    """
    # find the requested routine in the database and assign it to a variable
    routine = mongo.db.routines.find_one({"_id": ObjectId(routine_id)})
    # check current user is the user who created the routine
    if routine["username"] == session["user"]:
        # find all workout logs matching the given routine _id and delete
        mongo.db.workout_logs.delete_many({"routine_id": ObjectId(routine_id)})
        # delete the routine
        mongo.db.routines.delete_one(routine)
        flash("Routine and workout logs deleted.")
        return redirect(url_for("my_routines"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
