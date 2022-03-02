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
            if check_password_hash(valid_username["password"], request.form.get("password")):
                session["user"] = username
                flash(f"Welcome, {username}")
                return redirect(url_for('home'))
            else:
                flash(f"Username or password incorrect. Please try again.")
                return redirect(url_for('login'))
        else:
            flash(f"Username or password incorrect. Please try again.")
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
        # Assign submitted username to a variable and check if it exists in the database
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
            "routines": [
                {
                    "_id": ObjectId(),
                    "routine_name": "Beginner",
                    "exercise_one": "Chin-up",
                    "exercise_one_reps": 1,
                    "exercise_two": "Push-up",
                    "exercise_two_reps": 2,
                    "exercise_three": "Squat",
                    "exercise_three_reps": 3,
                    "preset": True
                },
                {
                    "_id": ObjectId(),
                    "routine_name": "Intermediate 1",
                    "exercise_one": "Chin-up",
                    "exercise_one_reps": 2,
                    "exercise_two": "Push-up",
                    "exercise_two_reps": 4,
                    "exercise_three": "Squat",
                    "exercise_three_reps": 6,
                    "preset": True
                },
                {
                    "_id": ObjectId(),
                    "routine_name": "Intermediate 2",
                    "exercise_one": "Pull-up",
                    "exercise_one_reps": 2,
                    "exercise_two": "Close Grip Push-up",
                    "exercise_two_reps": 4,
                    "exercise_three": "Lunge",
                    "exercise_three_reps": 6,
                    "preset": True
                }
            ]
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
            "$match": {"username": session['user']}
        },
        {
            "$lookup": {
                "from": "routines",
                "localField": "routine_id",
                "foreignField": "_id",
                "as": "routine"
            }
        }]))
    return render_template('workout_log.html', page_title="Workout Log", logs=logs)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
