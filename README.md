# Fitrio Fitness Tracker Application

[Visit the live site](https://fitrio.lmjh.dev/).

The purpose of this application is to help people get fit and track their progress with simplified bodyweight circuit training that can be done at home. The world of exercise and fitness can be intimidating to newcomers and has many barriers to entry, like expensive equipment or overwhelmingly complicated routines.

This application aims to solve this problem by encouraging people to try more focused circuit training consisting of just three exercises per routine.

* Three basic routines are provided, using compound exercises selected to cover as broad a range of muscle groups as possible
* Users can add their own routines.
* The only equipment required for the provided routines is a pull-up bar, which is cheap and readily available.
* Workouts are time-limited and users record the number of exercises they completed in the time limit.
* As users master the exercises and improve their fitness, their recorded number of sets for each routine should gradually increase. Fitrio generates progress graphs from the recorded data to allow users to visualise their progress.
* Progress pages with graphs and Personal Best scores can be shared with others.

![Mockup of Fitrio on desktop, tablet and mobile](documentation/readme-images/mockups/fitrio-mockup.png)

***

## User Experience

### New User Stories

* As a new user, I want to quickly understand the purpose of the site so that I can decide if it provides value to me.
* As a new user, I want to be able to quickly understand how to use the application to meet my needs.
* As a new user, I want clear instructions on how to perform the featured exercises and record my progress.
* As a new user, I want to know where to look for more information and help if I don’t understand something.

### Returning User Stories

* As a returning user, I want to be able to quickly access the features I’m interested in.
* As a returning user, I want to be able to easily access and manage the data I’ve saved in the application.
* As a returning user, I want to be able to create and manage my own custom routines
* As a returning user, I want to be able to assess my progress so I can see if the app is providing value for me
* As a returning user, I want to be able to share my achievements with others

### Design

The site uses the Materialize framework and features a dark mode design. I used the [Materialize dark theme](https://material.io/design/color/dark-theme.html) guidance to inform my design decisions, though I deviated from a strict, direct implementation of the guidance in a few areas.

#### Colours and Shades

* The site uses three shades of grey on the site’s surfaces to create a sense of depth. The darkest grey sits on the lowest visual level, with the mid grey in the middle and the lighter grey on the top level.

* The sense of depth is reinforced by consistent use of two levels of drop shadows on site elements. Elements with the shadow further from the element appear further from the surface they sit on, while elements with a closer drop shadow appear closer.

![Three shades of grey and drop shadows on the My Routines page](documentation/readme-images/design/design-1.jpg)

* I’ve tried to use shadows consistently, so card panels / surfaces in the mid grey colour sit far from their base layer, while the card panels/surfaces in the light grey sit closer to the mid grey surfaces beneath them. Buttons are always high above their parent elements for emphasis.

* In places, such as the graphs on the Track Progress pages, I’ve created a ‘cut-out’ effect using an inner drop shadow and colouring the inner element with the bottom grey shade.

!['Cut-out' visual effect on the progress graph](documentation/readme-images/design/design-2.jpg)

* In line with the Material Design dark theme guidance, I’ve used mostly light, desaturated colours.

* Colours are used consistently in association with a particular type of task:

* Light green is used on all buttons and flash messages associated with Create / Add operations, like adding a workout log or a new routine.

* Light blue is used on all buttons and flash messages associated with Read / Review operations, like searching the logs or tracking progress.

* Light amber is used on all buttons and flash messages associated with Update / Edit operations, like editing logs or routines, or updating sharing settings.

* Light red is used on all buttons and flash messages associated with Delete / Remove operations, like deleting logs or routines. Light red is also used for error messages.

![Buttons on the My Routine page, coloured according to function](documentation/readme-images/design/design-3.jpg)

* A light grey is used for neutral buttons, like ‘Cancel’ buttons. This creates a clear visual contrast between confirmation and cancellation in the confirmation modals for editing or deleting records.

![Grey cancel button provides visual contrast with red confirmation button](documentation/readme-images/design/design-4.jpg)

* Finally, a brighter, more saturated blue is used occasionally for emphasis. This is a brand colour and is used in the logo, on the progress graphs and to make links stand out.

![Saturated blue used in logo](documentation/readme-images/design/design-5.jpg)

#### Typography

* The site logo and headings use the [Cantarell font](https://fonts.google.com/specimen/Cantarell) from Google Fonts. This font was selected for its high legibility and simple, clean lines.
* All other text on the site uses the standard Materialize framework font stack, which consists of a number of simple, legible sans-serif fonts targeted at a range of different viewing devices and operating systems.

#### Imagery

* [Font Awesome 6](https://fontawesome.com/) icons are used throughout the site to illustrate buttons.
* Illustrative screenshots are included in the “how to log your workouts” section of the Getting Started page and in some FAQ sections.
* The “how it works” section of the Getting Started page is illustrated with drawings of clocks representing the time each stage should take. These illustrations were drawn as vectors with [Affinity Designer](https://affinity.serif.com/en-gb/designer/) in a style intended to match and complement the other site elements.

### Wireframes

The site is responsively designed to adapt to the user's viewing device.

| Page             |                            Wireframe                            |
|------------------|:---------------------------------------------------------------:|
| Home             | ![](documentation/readme-images/wireframes/home.png)            |
| Register         | ![](documentation/readme-images/wireframes/register.png)        |
| Login            | ![](documentation/readme-images/wireframes/log-in.png)          |
| Workout Log      | ![](documentation/readme-images/wireframes/workout-log.png)     |
| Add/Edit Workout | ![](documentation/readme-images/wireframes/add-workout.png)     |
| My Routines      | ![](documentation/readme-images/wireframes/my-routines.png)     |
| Add/Edit Routine | ![](documentation/readme-images/wireframes/add-routine.png)     |
| Track Progress   | ![](documentation/readme-images/wireframes/track-progress.png)  |
| Getting Started  | ![](documentation/readme-images/wireframes/getting-started.png) |
| FAQ              | ![](documentation/readme-images/wireframes/faq.png)             |

***

## Features

### User Accounts

Fitrio features a user account system whereby users can create a persistent account, accessed by username and password, and store data associated with their account.

* Users create accounts by filling in a simple registration form.

![Registration form](documentation/readme-images/features/user-accounts-register.jpg)

* Users sign in to their accounts by filling in a login form and sign out using a link in the navigation bar.

![Login form](documentation/readme-images/features/user-accounts-login.jpg)

* The application uses the Flask session object to handle user login functionality and passwords are hashed using Werkzeug helper functions.

### Workout Log

The core feature of Fitrio is a workout log allowing users to record their workouts. Full CRUD (create, read, update, delete) functionality is implemented for workout logs, so users can add, delete and edit their records as they wish.

* Workouts logs are added by completing a form, which is linked to from buttons on the Workout Log and My Routines pages.

![Add workout logs by filling a form](documentation/readme-images/features/workout-log-add-form.jpg)

* All workout logs are listed on the Workout Log page.

![List of workout logs](documentation/readme-images/features/workout-log-list.jpg)

* The workout logs are paginated and displayed in batches of ten to prevent pages becoming too large as more records are added.

![Log pagination with buttons to view older/newer logs](documentation/readme-images/features/workout-log-pagination.jpg)

* Workout logs can be filtered by date

![Log from and to date filter](documentation/readme-images/features/workout-log-filter.jpg)

* Individual workout records can be expanded by clicking or pressing enter on the keyboard when focused. The app calculates and displays the total number of exercise reps that were done for each log entry. The record can be edited or deleted by clicking the buttons here.

![An expanded workout log entry showing workout details and edit and delete buttons](documentation/readme-images/features/workout-log-expanded.jpg)

* When editing a log entry, the form is prepopulated with the current values of that log.

![Prepopulated edit log form](documentation/readme-images/features/workout-log-edit-form.jpg)

### Routine Management

A routine in Fitrio is a set of three exercises with an associated number of repetitions for each. Users select a routine whenever they log a workout.

* All users have access to three preset / default routines, which are displayed on the My Routines page and can be selected when adding a workout log.

![User view of preset routines](documentation/readme-images/features/routine-management-user-defaults.jpg)

* By design, users cannot edit or delete the default routines, as they are intended to be the basic foundational routines of the application that all users always have access to. However, the ‘admin’ user account can add, edit or delete default routines. This allows the site admin to make changes to the preset routines or add additional preset routines that will be automatically distributed to all other users.

![Admin view of preset routines](documentation/readme-images/features/routine-management-admin-defaults.jpg)

* Users can add their own custom routines by clicking the link in the My Routines page and then filling out a form.

![Add a routine by completing a form](documentation/readme-images/features/routine-management-add-routine.jpg)

* Full CRUD functionality is implemented for users’ own custom routines. Custom routines can be deleted or edited by clicking the appropriate buttons on the My Routines page.

![Delete or edit custom routines](documentation/readme-images/features/routine-management-custom-edit-delete.jpg)

*  When editing a routine, the form is prepopulated with the current values of that routine.

![Edit routine forms are prepopulated](documentation/readme-images/features/routine-management-edit-prepopulated.jpg)

### Track and Share Progress

Users can track their progress with Fitrio routines (both preset and custom routines) by clicking the ‘Track’ link present on each routine on the My Routines page.

* Progress for each routine is visualised with a line chart. This chart plots the number of sets completed against the date/time for each workout logged by the given user with the given routine.

![A chart visualises progress data](documentation/readme-images/features/track-progress-chart.jpg)

* A ‘personal best’ section displays the details of the workout with the highest number of sets that the user has recorded with this routine. Where multiple logs have the same highest number of sets, the log with the earliest date is used.

![Personal best statistics are displayed](documentation/readme-images/features/track-progress-best.jpg)

* By default, Track Progress pages cannot be viewed by any user except the page owner. However, users can click a “Share Page” button on the Track Progress page if they want to  share their progress. The page will then be viewable by any other logged in user who visits the page URL.

![Users can choose to share their progress](documentation/readme-images/features/track-progress-share.jpg)

* For convenience, pages which are currently shared show a link that users can copy. The “Share Page” button is also replaced with a “Hide Page” button, which can be clicked to hide the page at any time. The “Hide Page” button is only visible to the page owner.

![Users can choose to hide their progress](documentation/readme-images/features/track-progress-link-and-hide.jpg)

### Tutorials and FAQ

New users are redirected to a ‘Getting Started’ page after registration to help them learn how Fitrio works. An FAQ page is also provided with answers to common questions.

* The Getting Started page provides a step by step run down of how to use Fitrio workout routines.

![Step by step instructions for workouts](documentation/readme-images/features/tutorials-how-it-works.jpg)

* The Getting Started page also provides instructions on how to record workouts in the workout log and track progress.

![Instructions for logging workouts](documentation/readme-images/features/tutorials-how-to-log.jpg)

* The FAQ page provides answers to common questions in a collapsible accordion. Users can find detailed instructions for the exercises in the preset routines here.

![FAQ accordion](documentation/readme-images/features/tutorials-faq.jpg)

* Succinct instructions on how to use the features of the page are included at the top of the Workout Log and My Routines pages.

![Instruction box](documentation/readme-images/features/tutorials-instructions-box.jpg)

### Confirmation Modals

To mitigate the risk of accidental data loss, confirmation modals are used for all potentially destructive actions, including editing and deleting workout logs and editing and deleting custom routines.

* To ensure that the interface options are clear to users, the confirmation buttons are clearly labelled with the action to be taken and always match the colouring and icon of the action trigger button that was pressed. The cancel button is always in a neutral grey colour.

![Delete log confirmation modal](documentation/readme-images/features/modals-delete-log.jpg)

* A confirmation modal is also included for the action of updating the sharing settings on the Track Progress pages.

![Share progress confirmation modal](documentation/readme-images/features/modals-share.jpg)

### Error Pages

Custom error pages are included to gracefully handle errors.

* A 404 - Not Found page will display when a user attempts to visit an unvalid URL.

![404 Page Not Found error page](documentation/readme-images/features/error-pages-404.jpg)

* A 500 - Internal Server Error will display for any unhandled exceptions that might occur.

![500 Internal Server Error page](documentation/readme-images/features/error-pages-500.jpg)

***

## Database Design

Fitrio uses the MongoDB non-relational database. Data is divided into three collections, with the following schema:

**users**
```
_id: <ObjectId>
username: <string>
email: <string>
password: <string>
shared_routines: <array>
```

**routines**
```
_id: <ObjectId>
routine_name: <string>
exercise_one: <string>
exercise_one_reps: <int32>
exercise_two: <string>
exercise_two_reps: <int32>
exercise_three: <string>
exercise_three_reps: <int32>
username: <string>
```

**workout_logs**
```
_id: <ObjectId>
routine_id: <ObjectId>
date: <date>
notes: <string>
sets: <int32>
username: <string>
```

Although MongoDB is a non-relational database, I have emulated some of the properties of a relational database by nesting the ObjectIds of routines in the workout_logs documents and in the shared_routines array of the users document to connect those documents. 

Adding 'username' as a string to the routines and workout_logs documents also serves to link the workout_logs and routines with their owners in the users collection. I chose to use username strings rather than the ObjectId of the users because it makes the database documents more human-readable and because, unlike the routine names, usernames are unique and cannot be changed. 

If a future update allowed changing of usernames or for some reason required allowing non-unique usernames, the username strings in the routines and workout_logs documents could be replaced with the ObjectIds of the users documents, to ensure that they are unique.

***

## Future Features

The following features could be added in the future, given more development time:

### 1. Account Management Tools

* Helpful account management tools could be provided, such as the ability to update usernames, email addresses and passwords.
* A password recovery by email function could also be provided. The [flask-security](https://pythonhosted.org/Flask-Security/features.html) extension can provide this functionality, as well as some other more advanced account management tools.

### 2. Additional Log Filters

* Users can currently filter the workout log page by date range, but additional filters could be provided.
* In particular, the ability to filter by routine could be helpful.
* Filtering by specific exercises or by notes content could also be considered.

### 3. More advanced graphs on Track Progress page

* Additional features could be added to the Track Progress graphs.
* Graphs currently chart all available data for the given routine, so the ability to request a specific date range could be useful.
* Other options include adding different types of graph.

### 4. Social media sharing

* Users can currently share their progress by turning on sharing for a track progress page and then sharing a link.
* It could be helpful to add share buttons from social networks to streamline the process of sharing.

### 5. Code optimization and refactoring

* This was my first major project using Python and Flask, so there are a few areas where I feel the code could be made neater and more efficient.
* In particular, more helper functions could be employed to avoid repeating common tasks across the different functions.

### 6. Routine Sharing

* A way for users to share the custom routines that they've designed could be included.
* This could be placed on a new "Community Routines" page, from which users could select routines from other users to add to their 'My Routines' collection.

***

## Technologies

### Languages Used

* [HTML5](https://en.wikipedia.org/wiki/HTML5)
* [CSS3](https://en.wikipedia.org/wiki/CSS)
* [JavaScript](https://en.m.wikipedia.org/wiki/JavaScript)
* [Python](https://en.m.wikipedia.org/wiki/Python_(programming_language))

### Frameworks, Libraries & Programs Used

1. [GitHub](https://github.com/) - Used for version control.
2. [GitPod](https://gitpod.io/) - Used to write all code and test before deploying to GitHub.
3. [Balsamiq](https://balsamiq.com/) - Used to produce design wireframes.
4. [Materialize](https://materializecss.com/) - Materialize CSS framework used extensively to create layout and styling of site.
5. [jQuery](https://jquery.com/) - Used to initialise Materialize components and validate select elements.
6. [Python 3.8](https://www.python.org/) - Used to code the application.
7. [MongoDB](https://www.mongodb.com/) - Used for the application's database.
7. [Flask](https://palletsprojects.com/p/flask/), [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) and [Werkzeug](https://palletsprojects.com/p/werkzeug/) - Used to build the main application structure, page templates (Jinja) and account security (Werkzeug).
8. [PyMongo](https://github.com/mongodb/mongo-python-driver) - Used to connect Python with MongoDB
9. [Railway](https://railway.app/) - Used to deploy the site.
10. [Chart.js](https://www.chartjs.org/) - Used to render the routine progress charts.
11. [Regexr](https://regexr.com/) - Used to assist with writing and testing regular expressions.
12. [Affinity Designer](https://affinity.serif.com/en-gb/designer/) - Used to design logo and illustrations and to resize screenshots.
13. [Tables Generator](https://www.tablesgenerator.com/markdown_tables) - Used to generate markdown tables for README.md and TESTING.md
14. [W3C.org](https://www.w3.org/) - W3C [HTML Validator](https://validator.w3.org/nu/) and [CSS Validator](https://jigsaw.w3.org/css-validator/validator) used to check HTML and CSS code for errors.
15. [JSHint](https://jshint.com/) - Used to check JavaScript for errors.
16. [PEP8 Online](http://pep8online.com/) - Used to check Python code for errors.
17. [GraphBerry](https://www.graphberry.com/item/flat-devices-mockup) - Used to source the device templates for the site mockup at the top of this readme.

***

## Testing

Please see [TESTING.md](TESTING.md) for details of tests performed and bugs fixed.

***

## Deployment

### Forking the GitHub Repository

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/lmjh/fitness-tracker)
2. At the top right of the page, click the "Fork" Button.
3. You should now have a copy of the original repository in your GitHub account.

### Making a Local Clone

You can download the project source code as a zip file by clicking the 'Code' dropdown at the top right of the file navigation window and selecting "Download as ZIP". You can then unzip that file to wherever you want your local copy to be.

If you have Git installed on your computer, you can clone the project by following these steps:

1. Log in to GitHub and locate the [repository](https://github.com/lmjh/fitness-tracker)
2. Click the 'Code' dropdown at the top right of the file navigation window.
3. Copy the link under 'Clone' and 'HTTPS' to clone the repository using HTTPS.
4. Open Git Bash
5. Change the current working directory to the location where you want the cloned directory to be made.
6. Type `git clone`, and then paste the URL you copied in Step 3.

```
$ git clone https://github.com/lmjh/fitness-tracker.git
```
7. Press Enter. Your local clone will be created.

Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/lmjh/fitness-tracker)

### Database Setup

The project uses MongoDB, so for either local or remote deployment you'll need a properly configured database.

1. If you don't have a MongoDB account, sign up for a free account at [MongoDB](https://www.mongodb.com/).
2. If you don't have any clusters, create a new cluster.
3. Add a new database to your cluster with the name: **fitness_tracker**
4. The fitness_tracker database should have three collections with the following setup:

**users**
```
_id: <ObjectId>
username: <string>
email: <string>
password: <string>
shared_routines: <array>
```

**routines**
```
_id: <ObjectId>
routine_name: <string>
exercise_one: <string>
exercise_one_reps: <int32>
exercise_two: <string>
exercise_two_reps: <int32>
exercise_three: <string>
exercise_three_reps: <int32>
username: <string>
```

**workout_logs**
```
_id: <ObjectId>
routine_id: <ObjectId>
date: <date>
notes: <string>
sets: <int32>
username: <string>
```

In order to connect to the database, you'll need to create a user and generate a MongoDB URI. 

#### Creating a Database User

1. Go to the Overview page of your cluster 
2. Click Database Access under Security in the side menu
3. Next click Add New Database User
4. Select Password as the authentication method and then enter a username and password
5. Under "Built-in role" select "Read and write to any database"
6. Click "Add User"

#### Generating a MongoDB URI

1. Go to the Overview page of your cluster
2. Click the "Connect" button
3. Select "Connect your application"
4. Make sure 'Python' is selected for the driver, then copy the URI provided in the box
5. Replace the "password" and "myFirstDatabase" parts of the URI with your database user's password and the name of your database

### Local Deployment

Follow the steps below to deploy the project locally using VSCode.

(N.B. These instructions are for deployment on a Windows system)

1. Download and install [VSCode](https://code.visualstudio.com/)
6. Open VSCode and click File > Open Folder, then select the folder containing your local cloned repository
7. Download and install [Python](https://www.python.org/downloads/)
8. Download and install the [VSCode Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
9. In VSCode, open the command palette (Ctrl + Shift + P on Windows) and search for the Python: Select Interpreter. Click it, then select the version of Python you have installed.
10. Open a terminal in VSCode and enter the following commands to create and activate a virtual environment:
```
py -3 -m venv .venv
.venv\scripts\activate
```
11. Open the command palette and search for Python: Select Interpreter again. You should see your new virtual environment. Select it.
12. In the terminal, enter the following command to install all required packages:
```
python -m pip install -r requirements.txt
```
13. Create a new file in your project directory called "env.py"
14. Add the following to the env.py file, replacing YOUR_MONGO_URI with your MongoDB URI, YOUR_DATABASE_NAME with your database name, and YOUR_SECRET_KEY with a suitable [secret key](https://flask.palletsprojects.com/en/2.0.x/config/#SECRET_KEY):
```
import os

os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", "YOUR_SECRET_KEY")
os.environ.setdefault("MONGO_URI", "YOUR_MONGO_URI")
os.environ.setdefault("MONGO_DBNAME", "YOUR_DATABASE_NAME")
os.environ.setdefault("ENV_DEBUG", "True")
```
15. In the terminal, type `python app.py` to run the app. A link to the locally running instance of the app should be printed in the terminal window.

***

## Other Credits and Acknowledgements

* My Code Institute mentor, [Tim Nelson](https://tim.2bn.dev/), for his very helpful advice and feedback throughout the project, as well as the Javascript code to validate the Materialize select elements.
* [Code Institute](https://codeinstitute.net/) for their helpful lessons and reference materials.
* [Code Institute Sample README](https://github.com/Code-Institute-Solutions/SampleREADME/blob/master/README.md) for the structure of this project's documentation and parts of the GitHub forking and cloning processes.
* [This blog post](https://www.patricksoftwareblog.com/creating-charts-with-chart-js-in-a-flask-application/) from Patrick's Software Blog provided some very helpful information on generating chart.js graphs with data from a Flask application.
* [This YouTube video](https://www.youtube.com/watch?v=H1y66SPBlRI) from the channel Chart JS provided some very helpful information on setting up a chart.js graph using datetime data for one of the axes.
