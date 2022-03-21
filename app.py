import os
import datetime
from functools import wraps
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


def login_required(f):
    """
    Decorator to check if a user is currently logged in and redirect to the
    login page if not.
    Based on this function from the Flask documetation:
    https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/#login-required-decorator
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            flash("You must login to access this page.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def find_user(username):
    """
    Helper function that searches the users collection for a record with a
    username matching the given username and returns the record if found.
    """
    # query database for username and return it
    user = mongo.db.users.find_one({"username": username})
    return user


def find_log(log_id):
    """
    Helper function that searches the workout_logs collection for a record with
    an ObjectId matching the given routine_id and returns the record if found.
    """
    # query database for log
    log = mongo.db.workout_logs.find_one({"_id": ObjectId(log_id)})

    # if log not found, raise a ValueError
    if log is None:
        raise ValueError('Invalid Log Id')
    return log


def find_routine(routine_id):
    """
    Helper function that searches the routines collection for a record with an
    ObjectId matching the given routine_id and returns the record if found.
    """
    # query database for routine
    routine = mongo.db.routines.find_one({"_id": ObjectId(routine_id)})

    # if routine not found, raise a ValueError
    if routine is None:
        raise ValueError('Invalid Routine Id')
    return routine


@app.route("/")
def home():
    """
    If user is logged in, redirects them to workout_log page. Otherwise,
    renders the home page.
    """
    # check if user is currently logged in
    if session.get("user") is None:
        return render_template("home.html", page_title="Home")

    # redirect already logged in users to workout_log page
    return redirect(url_for("workout_log"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    GET: If user is logged in, redirects them to workout_log page. Otherwise,
    renders the login page.
    POST: Collects submitted user credentials.
    If username and passsword are correct, user is logged in and redirected to
    the home page.
    If username and password are incorrect, user is redirected to the login
    page.
    """
    # check if user is currently logged in
    if session.get("user") is None:
        if request.method == "POST":
            # assign submitted username to a variable and query the database to
            # find a record with that name
            username = request.form.get("username").lower()
            valid_username = find_user(username)

            # check the submitted username exists in the database
            if valid_username:

                # check the submitted password matches the database
                if check_password_hash(
                        valid_username["password"],
                        request.form.get("password")):

                    # add user to session cookie and redirect to workout log
                    session["user"] = username
                    flash(f"Welcome, {username}", "message")
                    return redirect(url_for('workout_log'))

                # if submitted password is incorrect, return to login page
                flash("Username or password incorrect. Please try again.",
                      "error")
                return redirect(url_for('login'))

            # if submitted username is incorrect, return to login page
            flash("Username or password incorrect. Please try again.", "error")
            return redirect(url_for('login'))

        return render_template("login.html", page_title="Login")

    # redirect already logged in users to workout_log page
    return redirect(url_for("workout_log"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    GET: If user is logged in, redirects them to workout_log page. Otherwise,
    renders the registration page.
    POST: Collects submitted user data and checks if requested username is
    available.
    If username is taken, user is returned to the registration page.
    If username is available, a new user record is added to the users database
    and the user is logged in and redirected to the getting started page.
    """
    # check if user is currently logged in
    if session.get("user") is None:
        if request.method == "POST":
            # assign submitted username to a variable and check if it exists in
            # the database
            username = request.form.get("username").lower()
            duplicate_user = find_user(username)

            # if username already exists, return user to registration page
            if duplicate_user:
                flash(f"Username \"{username}\" is unavailable.", "error")
                return redirect(url_for("register"))

            # build dictionary with user submitted details
            new_user = {
                "username": username,
                "email": request.form.get("email"),
                "password": generate_password_hash(
                                request.form.get("password")),
                "shared_routines": []
            }

            # insert new user dict to users database
            mongo.db.users.insert_one(new_user)

            # add new user to session cookie and redirect to getting started
            session["user"] = username
            flash(
                f"Welcome, {session['user']}! Your account has been created.",
                "create")
            return redirect(url_for('getting_started'))

        return render_template("register.html", page_title="Register")

    # redirect logged in users to workout_log page
    return redirect(url_for("workout_log"))


@app.route('/logout')
@login_required
def logout():
    """
    Removes the user from the session cookie and redirects to the home page.
    """
    session.pop("user")
    flash("You have been logged out.", "message")
    return redirect(url_for('home'))


@app.route('/workout_log')
@login_required
def workout_log():
    """
    Finds workouts logged by the user and renders the workout log page.
    Reads query parameters from the URL to restrict results to a requested date
    range and/or paginate results.
    """
    # retrieve date_from and date_to values from query parameters if available
    # and assign to variables
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    # if date_from and date_to query parameters were found
    if date_from and date_to:
        # try to convert date_from and date_to to datetime objects
        try:
            date_from = datetime.datetime.strptime(date_from, "%d/%m/%y")
            date_to = datetime.datetime.strptime(date_to + "23:59:59",
                                                 "%d/%m/%y%H:%M:%S")
        except ValueError:
            # if either of the submitted dates aren't valid and in the correct
            # format, redirect user back to workout_log page with error message
            flash(
                "Invalid date. Please enter valid dates in the format."
                "dd/mm/yy.", "error")
            return redirect(url_for("workout_log"))

        # show an error message if date_to is earlier than date_from
        if date_to < date_from:
            flash("Search end date must be after start date.", "error")
            return redirect(url_for("workout_log"))

        # check if a skip query parameter is present and if so assign it to
        # a variable. Otherwise, set the skip variable to 0.
        if request.args.get("skip"):
            skip = int(request.args.get("skip"))
        else:
            skip = 0

        # query the database to count how many workouts have been logged by the
        # current user in the requested date range.
        count = mongo.db.workout_logs.count_documents(
            {
                "username": session['user'],
                "date": {
                    "$gte": date_from,
                    "$lt": date_to
                }
            })

        # pass date_from and date_to objects into database query
        # lookup corresponding routine details using routine_id
        # sort by date and use skip and limit to paginate results in batches
        # of 10
        logs = list(mongo.db.workout_logs.aggregate([
            {
                "$match": {
                    "username": session['user'],
                    "date": {
                        "$gte": date_from,
                        "$lt": date_to
                    }
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
            },
            {
                "$skip": skip
            },
            {
                "$limit": 10
            }
            ]))

        # pass the results of the query, the current skip value and the
        # document count to the workout_log template
        flash("Results updated.", "message")
        return render_template('workout_log.html', page_title="Workout Log",
                               logs=logs, skip=skip, count=count)

    # check if a skip query parameter is present and if so assign it to a
    # variable. Otherwise, set the skip variable to 0.
    if request.args.get("skip"):
        skip = int(request.args.get("skip"))
    else:
        skip = 0

    # query the database to count how many workouts have been logged by the
    # current user
    count = mongo.db.workout_logs.count_documents(
                                                 {"username": session['user']})

    # find all workouts logged by the current user
    # lookup corresponding routine details using routine_id
    # sort by date and use skip and limit to paginate results in batches of 10
    logs = list(mongo.db.workout_logs.aggregate([
        {
            "$match": {
                "username": session['user'],
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
        },
        {
            "$skip": skip
        },
        {
            "$limit": 10
        }
        ]))

    # pass the results of the query, the current skip value and the document
    # count to the workout_log template
    return render_template('workout_log.html', page_title="Workout Log",
                           logs=logs, skip=skip, count=count)


@app.route("/add_workout", methods=["GET", "POST"])
@login_required
def add_workout():
    """
    GET: Renders the Add Workout page
    POST: Collects user input, inserts to workout_logs database and redirects
    user to Workout Log page
    """
    if request.method == "POST":
        # concatenate date picker value and time picker value
        date = request.form.get("workout_date") + request.form.get(
                "workout_time")
        # try to convert concatenated date into ISODate
        try:
            iso_date = datetime.datetime.strptime(date, "%d/%m/%y%H:%M")
        except ValueError:
            # if either the date or the time isn't valid and in the correct
            # format, redirect user back to add_workout page with error message
            flash(
                "Invalid date/time. Please enter a valid date and time in the "
                "formats dd/mm/yy and hh:mm.", "error")
            return redirect(url_for("add_workout"))

        # build dictionary containing user submitted workout details
        entry = {
            "routine_id": ObjectId(request.form.get("routine_name")),
            "date": iso_date,
            "notes": request.form.get("notes"),
            "sets": int(request.form.get("sets")),
            "username": session['user']
        }

        # insert dictionary into database and redirect user to workout log
        mongo.db.workout_logs.insert_one(entry)
        flash("Workout log added.", "create")
        return redirect(url_for("workout_log"))

    # retrieve routine_name query parameter, if present
    routine_name = request.args.get('routine_name')

    # find default routines (created by admin) and convert cursor to a list
    default_routines = list(mongo.db.routines.find({"username": "admin"}))
    # find user's custom routines and convert cursor to a list
    user_routines = list(mongo.db.routines.find({"username": session['user']}))

    # concatenate default and custom routines lists, then pass with
    # routine_name to the add_workout template
    routines = default_routines + user_routines
    return render_template(
        "add_workout.html", page_title="Add Workout", routines=routines,
        routine_name=routine_name)


@app.route("/edit_workout/<log_id>", methods=["GET", "POST"])
@login_required
def edit_workout(log_id):
    """
    GET: Renders edit_workout page with data from requested log id
    POST: If current user created the log entry, updates the entry.
    Otherwise, returns user to workout log page.
    """
    # if log_id is not a valid objectid, redirect to workout_log
    if not ObjectId.is_valid(log_id):
        flash("Invalid Log ID.", "error")
        return redirect(url_for("workout_log"))

    # try to find log to edit from database
    # redirect to workout_log if Id is invalid
    try:
        log = find_log(log_id)
    except ValueError:
        flash("Invalid Log ID.", "error")
        return redirect(url_for("workout_log"))

    if request.method == "POST":
        # check current user is the user who created the entry
        if log["username"] == session["user"]:
            # concatenate date picker value and time picker value
            date = request.form.get("workout_date") + request.form.get(
                    "workout_time")

            # try to convert concatenated date into ISODate
            try:
                iso_date = datetime.datetime.strptime(date, "%d/%m/%y%H:%M")
            except ValueError:
                # if either the date or the time isn't valid and in the correct
                # format, redirect user back to edit_workout page with error
                # message
                flash(
                    "Invalid date/time. Please enter a valid date and time in "
                    "the formats dd/mm/yy and hh:mm.", "error")
                return redirect(url_for("edit_workout", log_id=log_id))

            # build dictionary from user submitted workout details
            entry = {
                "routine_id": ObjectId(request.form.get("routine_name")),
                "date": iso_date,
                "notes": request.form.get("notes"),
                "sets": int(request.form.get("sets")),
                "username": session['user']
            }

            # update the database entry with the entered details and redirect
            # user to workout log
            mongo.db.workout_logs.update_one(log, {"$set": entry})
            flash("Workout log updated.", "edit")
            return redirect(url_for("workout_log"))

        # redirect unauthorised users to workout log page
        flash("You don't have permission to edit this log.", "error")
        return redirect(url_for("workout_log"))

    # find default routines (created by admin) and convert cursor to a list
    default_routines = list(mongo.db.routines.find({"username": "admin"}))
    # find user's custom routines and convert cursor to a list
    user_routines = list(mongo.db.routines.find({"username": session['user']}))
    # concatenate default and custom routines lists, then pass to the
    # edit_workout template
    routines = default_routines + user_routines
    return render_template(
        "edit_workout.html", page_title="Edit Workout", log=log,
        routines=routines)


@app.route("/delete_workout/<log_id>")
@login_required
def delete_workout(log_id):
    """
    Checks if current user created the log entry to be deleted and deletes it
    if so. Otherwise, returns user to workout log page.
    """
    # if log_id is not a valid objectid, redirect to workout_log
    if not ObjectId.is_valid(log_id):
        flash("Invalid Log ID.", "error")
        return redirect(url_for("workout_log"))

    # try to find log to delete from database
    # redirect to workout_log if Id is invalid
    try:
        log = find_log(log_id)
    except ValueError:
        flash("Invalid Log ID.", "error")
        return redirect(url_for("workout_log"))

    # check current user is the user who created the entry
    if log["username"] == session["user"]:
        # delete log entry from database and redirect user to workout log
        mongo.db.workout_logs.delete_one(log)
        flash("Workout log deleted.", "delete")
        return redirect(url_for("workout_log"))

    # redirect unauthorised users to workout log page
    flash("You don't have permission to delete this log.", "error")
    return redirect(url_for("workout_log"))


@app.route("/my_routines")
@login_required
def my_routines():
    """
    Finds all default (admin created) routines and all routines created by the
    user and renders the my_routines page
    """
    # query database to find all admin created routines
    default_routines = list(mongo.db.routines.find({"username": "admin"}))
    # query database to find all routines created by current user
    custom_routines = list(mongo.db.routines.find(
                        {"username": session["user"]}))
    # pass default and custom routines to the my_routines template
    return render_template("my_routines.html", page_title="My Routines",
                           default_routines=default_routines,
                           custom_routines=custom_routines)


@app.route("/add_routine", methods=["GET", "POST"])
@login_required
def add_routine():
    """
    GET: Render the add_routine page
    POST: Checks if the submitted routine name is the same as any admin
    routines or routines by the current user. If so, user is redirected back to
    the add_routine page. If not, the routine is added to the database.
    """
    if request.method == "POST":
        # assign submitted routine name to a variable and check if the current
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

        # if a record is found matching current user and routine name or admin
        # and routine name, redirect to add_routine page
        if duplicate_routine:
            flash(
                "Duplicate routine name. Please enter a unique routine name.",
                "error")
            return redirect(url_for("add_routine"))

        # build dictionary from user's entered data
        new_routine = {
            "routine_name": routine_name,
            "exercise_one": request.form.get("exercise_one"),
            "exercise_one_reps": int(request.form.get("exercise_one_reps")),
            "exercise_two": request.form.get("exercise_two"),
            "exercise_two_reps": int(request.form.get("exercise_two_reps")),
            "exercise_three": request.form.get("exercise_three"),
            "exercise_three_reps": int(
                                    request.form.get("exercise_three_reps")),
            "username": session["user"]
        }

        # insert new routine dictionary to database and redirect user to
        # my_routines page
        mongo.db.routines.insert_one(new_routine)
        flash("New routine successfully added.", "create")
        return redirect(url_for("my_routines"))

    return render_template("add_routine.html", page_title="Add Routine")


@app.route("/edit_routine/<routine_id>", methods=["GET", "POST"])
@login_required
def edit_routine(routine_id):
    """
    GET: Renders edit_routine page with data from requested routine id
    POST: If current user did not create the requested routine or if the
    submitted routine name is the same as any admin routines or other routines
    by the current user, the user is redirected to the my_routines page.
    Otherwise, the requested routine is updated with the submitted details.
    """
    # if routine_id is not a valid objectid, redirect to my_routines
    if not ObjectId.is_valid(routine_id):
        flash("Invalid Routine ID.", "error")
        return redirect(url_for("my_routines"))

    # find routine to edit from database
    # redirect to my_routines if Id is invalid
    try:
        routine = find_routine(routine_id)
    except ValueError:
        flash("Invalid Routine ID.", "error")
        return redirect(url_for("my_routines"))

    if request.method == "POST":
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
                        " name.", "error")
                    return redirect(url_for(
                        "edit_routine", routine_id=routine_id))

            # build dictionary containing sumitted routine details
            entry = {
                "routine_name": routine_name,
                "exercise_one": request.form.get("exercise_one"),
                "exercise_one_reps": int(request.form.get(
                                        "exercise_one_reps")),
                "exercise_two": request.form.get("exercise_two"),
                "exercise_two_reps": int(request.form.get(
                                        "exercise_two_reps")),
                "exercise_three": request.form.get("exercise_three"),
                "exercise_three_reps": int(request.form.get(
                                        "exercise_three_reps")),
                "username": session["user"]
            }
            flash("Routine updated.", "edit")
            # update the database entry with the entered details
            mongo.db.routines.update_one(routine, {"$set": entry})
            return redirect(url_for("my_routines"))

        # redirect unauthorised users to workout log page
        flash("You don't have permission to edit this routine.", "error")
        return redirect(url_for("my_routines"))

    return render_template(
        "edit_routine.html", page_title="Edit Routine", routine=routine)


@app.route("/delete_routine/<routine_id>")
@login_required
def delete_routine(routine_id):
    """
    If current user created the requested routine, deletes the routine and all
    logs using that routine from the database, then redirects the user to the
    my_routines page. Otherwise, redirects user to my_routines page with an
    error message.
    """
    # if routine_id is not a valid objectid, redirect to my_routines
    if not ObjectId.is_valid(routine_id):
        flash("Invalid Routine ID.", "error")
        return redirect(url_for("my_routines"))

    # try to find routine to delete from database
    # redirect to my_routines if Id is invalid
    try:
        routine = find_routine(routine_id)
    except ValueError:
        flash("Invalid Routine ID.", "error")
        return redirect(url_for("my_routines"))

    # check current user is the user who created the routine
    if routine["username"] == session["user"]:
        # find all workout logs matching the given routine _id and delete
        mongo.db.workout_logs.delete_many({"routine_id": ObjectId(routine_id)})

        # delete the routine and redirect user to my_routines page
        mongo.db.routines.delete_one(routine)
        flash("Routine and workout logs deleted.", "delete")
        return redirect(url_for("my_routines"))

    # redirect unauthorised users to my_routines page
    flash("You don't have permission to delete this routine.", "error")
    return redirect(url_for("my_routines"))


@app.route("/track_progress/<username>/<routine_id>")
def track_progress(username, routine_id):
    """
    Check if the current user is the page owner or if the page owner has shared
    the page. If so, proceed, if not, redirect user to my_routines page.
    If the page owner has recorded workouts with the given routine, collect
    data from the database and pass it to the track_progress page template.
    If the user hasn't recorded any data for this routine, redirect to the
    my_routines page.
    """
    # find the page owner in the users database
    user = find_user(username)

    # if username is not valid or routine id is not valid, redirect to home
    if not user or not ObjectId.is_valid(routine_id):
        flash("Invalid Username or Routine ID.", "error")
        return redirect(url_for("home"))

    # if a user is logged in, determine if they are the page owner
    if session.get("user"):
        owner = username == session["user"]
    else:
        owner = False

    # determine if the page has been shared by its owner
    shared = routine_id in user["shared_routines"]

    # if either the current user is the page owner or the page owner has shared
    # the page, proceed to display the page.
    if owner or shared:
        # query the database for records matching both the username and
        # routine_id provided, sort by date then convert results to a list
        logs = list(mongo.db.workout_logs.find(
            {
                "$and": [
                    {
                        "username": username
                    },
                    {
                        "routine_id": ObjectId(routine_id)
                    }
                ]
            }).sort("date"))

        # if results were found
        if logs:
            # declare lists to store chart labels and values
            dates = []
            sets = []
            # iterate through list of workout logs and append dates to dates
            # list and sets to sets list
            for log in logs:
                dates.append(log["date"])
                sets.append(log["sets"])

            # use the python max() function on the list of logs to assign the
            # record with the highest number of sets to a variable, in order to
            # show a 'personal best' score on the track_progress page.
            # based on this answer from StackOverflow:
            # https://stackoverflow.com/a/5326622
            best = max(logs, key=lambda x: x['sets'])

            # query the database to find the applicable routine and assign to a
            # variable
            routine = find_routine(routine_id)

            # gather data in a dict and pass to template
            data = {
                "owner": owner,
                "shared": shared,
                "best": best,
                "dates": dates,
                "sets": sets,
                "routine": routine,
                "username": username
            }
            return render_template("track_progress.html", data=data,
                                   page_title="Track Progress")

        # if no results found, redirect user to my_routines page
        flash("No workouts logged with this routine.", "error")
        return redirect(url_for("my_routines"))

    # if user is not owner and page is not shared, redirect to home
    flash("You don't have permission to view that page.", "error")
    return redirect(url_for("home"))


@app.route("/toggle_sharing/<username>/<routine_id>")
@login_required
def toggle_sharing(username, routine_id):
    """
    If current user is the page owner, toggles sharing on/off for the given
    username and routine pair by adding or removing the routine's object id to
    an array in the user's database document.
    """
    # find the user in the users database
    user = find_user(username)

    # if username is not valid or routine id is not valid, redirect to
    # my_routines
    if not user or not ObjectId.is_valid(routine_id):
        flash("Invalid Username or Routine ID.", "error")
        return redirect(url_for("my_routines"))

    # check current user is the owner of the track_progress page
    if username == session["user"]:

        # check routine exists in the database
        # redirect to my_routines if Id is invalid
        try:
            find_routine(routine_id)
        except ValueError:
            flash("Invalid Routine ID.", "error")
            return redirect(url_for("my_routines"))

        # If the routine_id is in the shared_routines array, remove it.
        if routine_id in user["shared_routines"]:
            mongo.db.users.update_one(
                {
                    "username": username
                },
                {
                    "$pull": {
                        'shared_routines': routine_id
                    }
                })
            flash("Settings updated. This page is now private.", "edit")
            return redirect(url_for("track_progress", username=username,
                                    routine_id=routine_id))

        # If the routine_id is not in the shared_routines array, add it.
        mongo.db.users.update_one(
                {
                    "username": username
                },
                {
                    "$push": {
                        'shared_routines': routine_id
                    }
                })

        flash("Settings updated. This page can now be shared via link.",
              "edit")
        return redirect(url_for("track_progress", username=username,
                        routine_id=routine_id))

    flash("You don't have permission to edit that user's share settings.",
          "error")
    return redirect(url_for("my_routines"))


@app.route("/getting_started")
def getting_started():
    """
    Renders the getting_started page.
    """
    return render_template('getting_started.html',
                           page_title="Getting Started")


@app.route("/faq")
def faq():
    """
    Renders the faq page.
    """
    return render_template('faq.html',
                           page_title="Frequently Asked Questions")


@app.errorhandler(404)
def page_not_found(error):
    """
    Renders an error page when a 404 exception is raised.
    Based on the examples in the Flask documentation:
    https://flask.palletsprojects.com/en/2.0.x/errorhandling/
    """
    return render_template('errors/404.html', page_title="Page Not Found"), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    Renders an error page when a 500 exception is raised.
    Based on the examples in the Flask documentation:
    https://flask.palletsprojects.com/en/2.0.x/errorhandling/
    """
    return render_template('errors/500.html',
                           page_title="Internal Server Error"), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("ENV_DEBUG"))
