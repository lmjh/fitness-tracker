# Fitrio Fitness Tracker Application

The purpose of this application is to help people get fit and track their progress with simplified bodyweight circuit training that can be done at home. The world of exercise and fitness can be intimidating to newcomers and has many barriers to entry, like expensive equipment or overwhelmingly complicated routines. 

This application aims to solve this problem by encouraging people to try more focused circuit training consisting of just three exercises per routine. 

* Three basic routines are provided, using compound exercises selected to cover as broad a range of muscle groups as possible
* Users can add their own routines. 
* The only equipment required for the provided routines is a pull-up bar, which is cheap and readily available.
* Workouts are time-limited and users record the number of exercises they completed in the time limit.
* Users can clearly see their progress as their recorded number of sets for each routine will gradually increase as they master the exercises and improve their fitness.

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

### Design

The site uses the Materialize framework and features a dark mode design. I used the [Materialize dark theme](https://material.io/design/color/dark-theme.html) guidance to inform my design decisions, though I deviated from a strict, direct implementation of the guidance in a few areas.

#### Colours and Shades

* The site uses three shades of grey on the site’s surfaces to create a sense of depth. The darkest grey sits on the lowest visual level, with the mid grey in the middle and the lighter grey on the top level.

* The sense of depth is reinforced by consistent use of two levels of drop shadows on site elements. Elements with the shadow further from the element appear further from the surface they sit on, while elements with a closer drop shadow appear closer. 

![Three shades of grey and drop shadows on the My Routines page](documentation/readme-images/design-1.jpg)

* I’ve tried to use shadows consistently, so card panels / surfaces in the mid grey colour sit far from their base layer, while the card panels/surfaces in the light grey sit closer to the mid grey surfaces beneath them. Buttons are always high above their parent elements for emphasis. 

* In places, such as the graphs on the Track Progress pages, I’ve created a ‘cut-out’ effect using an inner drop shadow and colouring the inner element with the bottom grey shade.

!['Cut-out' visual effect on the progress graph](documentation/readme-images/design-2.jpg)

* In line with the Material Design dark theme guidance, I’ve used mostly light, desaturated colours.

* Colours are used consistently in association with a particular type of task:

* Light green is used on all buttons and flash messages associated with Create / Add operations, like adding a workout log or a new routine.

* Light blue is used on all buttons and flash messages associated with Read / Review operations, like searching the logs or tracking progress.

* Light amber is used on all buttons and flash messages associated with Update / Edit operations, like editing logs or routines, or updating sharing settings.

* Light red is used on all buttons and flash messages associated with Delete / Remove operations, like deleting logs or routines. Light red is also used for error messages.

![Buttons on the My Routine page, coloured according to function](documentation/readme-images/design-3.jpg)

* A light grey is used for neutral buttons, like ‘Cancel’ buttons. This creates a clear visual contrast between confirmation and cancellation in the confirmation modals for editing or deleting records.

![Grey cancel button provides visual contrast with red confirmation button](documentation/readme-images/design-4.jpg)

* Finally, a brighter, more saturated blue is used occasionally for emphasis. This is a brand colour and is used in the logo, on the progress graphs and to make links stand out.

![Saturated blue used in logo](documentation/readme-images/design-5.jpg)

#### Typography

* The site logo and headings use the [Cantarell font](https://fonts.google.com/specimen/Cantarell) from Google Fonts. This font was selected for its high legibility and simple, clean lines.
* All other text on the site uses the standard Materialize framework font stack, which consists of a number of simple, legible sans-serif fonts targeted at a range of different viewing devices and operating systems.

#### Imagery

* [Font Awesome 6](https://fontawesome.com/) icons are used throughout the site to illustrate buttons.
* Illustrative screenshots are included in the “how to log your workouts” section of the Getting Started page and in some FAQ sections.
* The “how it works” section of the Getting Started page is illustrated with drawings of clocks representing the time each stage should take. These illustrations were drawn as vectors with [Affinity Designer](https://affinity.serif.com/en-gb/designer/) in a style intended to match and complement the other site elements.

### Wireframes

The site is responsively designed to adapt to the user's viewing device. Wireframes for each page can be viewed [here](documentation/wireframes/).

***

## Features



***

## Technologies

### Languages Used

* HTML5
* CSS3
* Javascript
* Python

### Frameworks, Libraries & Programs Used

1. [GitHub](https://github.com/) - Used for version control.
2. [GitPod](https://gitpod.io/) - Used to write all code and test before deploying to GitHub.
3. [Balsamiq](https://balsamiq.com/) - Used to produce design wireframes.
4. [Materialize](https://materializecss.com/) - Materialize CSS framework used extensively to create layout and styling of site.
5. [jQuery](https://jquery.com/) - 
6. [Python 3.8](https://www.python.org/) - Used to code the application.
7. [Flask](https://palletsprojects.com/p/flask/), [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) and [Werkzeug](https://palletsprojects.com/p/werkzeug/) - Used to build the main application structure, page templates (Jinja) and account security (Werkzeug).
8. [PyMongo](https://github.com/mongodb/mongo-python-driver) - 
9. [Heroku](https://heroku.com/) - Used to deploy the site.
10. [Chart.js](https://www.chartjs.org/) - Used to render the routine progress charts.
11. [Regexr](https://regexr.com/) - Used to assist with writing and testing regular expressions.
12. [Affinity Designer](https://affinity.serif.com/en-gb/designer/) - Used to design logo and illustrations and to resize screenshots.

***

## Testing

Please see TESTING.md for details of tests performed and bugs fixed.

***

## Deployment

***

## Other Credits and Acknowledgements