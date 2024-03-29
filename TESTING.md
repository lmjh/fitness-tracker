# Testing of Fitrio Fitness Tracker
## Code Validation

* HTML code validated with W3C [HTML Validator](https://validator.w3.org/nu/).

* CSS code validated with W3C [CSS Validator](https://jigsaw.w3.org/css-validator/).

* Javascript code validated with [JSHint](https://jshint.com/).

* Python code validated with [PEP8 Online](http://pep8online.com/).

### HTML Validation

Because the raw html files contained jinja template code which would prevent proper validation, HTML validation was done by opening the page to be validated in a browser, then opening the page source code from the browser window and copying that into the W3C HTML Validator.

| Page                 |                                 Screenshot                                 | Notes               |
|----------------------|:--------------------------------------------------------------------------:|---------------------|
| home.html            | ![](documentation/testing-images/html-validation/home-html.jpg)            |                     |
| register.html        | ![](documentation/testing-images/html-validation/register-html.jpg)        |                     |
| login.html           | ![](documentation/testing-images/html-validation/login-html.jpg)           |                     |
| workout_log.html     | ![](documentation/testing-images/html-validation/workout-log-html.jpg)     | Aria label warnings |
| add_workout.html     | ![](documentation/testing-images/html-validation/add-workout-html.jpg)     |                     |
| edit_workout.html    | ![](documentation/testing-images/html-validation/edit-workout-html.jpg)    |                     |
| my_routines.html     | ![](documentation/testing-images/html-validation/my-routines-html.jpg)     |                     |
| add_routine.html     | ![](documentation/testing-images/html-validation/add-routine-html.jpg)     |                     |
| edit_routine.html    | ![](documentation/testing-images/html-validation/edit-routine-html.jpg)    |                     |
| track_progress.html  | ![](documentation/testing-images/html-validation/track-progress-html.jpg)  |                     |
| getting_started.html | ![](documentation/testing-images/html-validation/getting-started-html.jpg) |                     |
| faq.html             | ![](documentation/testing-images/html-validation/faq-html.jpg)             | Aria label warnings |
| 404.html             | ![](documentation/testing-images/html-validation/404-html.jpg)             |                     |
| 500.html             | ![](documentation/testing-images/html-validation/500-html.jpg)             |                     |

All page validation passed with no errors.

A warning was returned for all collapsibles on the FAQ and Workout Log pages, which reads:

"Possible misuse of aria-label. (If you disagree with this warning, file an issue report or send e-mail to www-validator@w3.org.)"

This warning is being raised because I added an aria-label to the header of each collapsible which reads "Click to open or close question/log entry". I think this is appropriate use of the aria-label based on the [W3C Web Content Accessibility Guidelines](https://www.w3.org/TR/WCAG20-TECHS/ARIA14.html):

"elements can be given the attribute aria-label to provide an accessible name for situations when there is no visible label due to a chosen design approach or layout but the context and visual appearance of the control make its purpose clear."

In my case, the collapsible header is an interactive element which opens and closes the collapsible. This behaviour is made clear visually by the chevron symbol on the right side. The aria-label makes the behaviour clear to users who cannot see the symbol.

### CSS Validation

CSS validation passed with no errors.

![CSS validation screenshot](documentation/testing-images/css-validation/css-validation.jpg)

8 warnings were returned:

![CSS warnings](documentation/testing-images/css-validation/css-warnings.jpg)

The first of these warnings, that "the property clip is deprecated" refers to the 'visually-hidden' class that I borrowed from the Bootstrap framework. This class hides elements from the visual flow of the document, but keeps them accessible to assistive technologies like screenreaders.

There are a few threads discussing this issue on the Bootstrap GitHub page (such as [this one](https://github.com/twbs/bootstrap/issues/27177)) and it seems that although `clip` is officially deprecated, it is more widely supported by browsers that its replacement, `clip-path`. The site caniuse.com lists [full support for clip](https://caniuse.com/mdn-css_properties_clip) from most browsers, but only [partial support for clip-path](https://caniuse.com/css-clip-path). I chose to stick with the Bootstrap implementation of the visually-hidden class on this basis.

The other seven warnings only refer to vendor prefixes, which are provided as fallbacks for some css properties.

### Javascript Validation

The script.js file, which initialises most Materialize javascript components and contains the code to validate Materialize select elements, was validated by copying its contents into JSHint.

The javascript that renders the chart.js charts on the Track Progress pages contains jinja templating code which would prevent proper validation with JSHint. I therefore validated this code by opening a Track Progress page in a browser and copying the javascript code from the source file (with injected values from jinja), then pasting that into JSHint.

The javascript that initialises the datepickers on the Workout Log and Edit Workout pages also contains jinja templating code, but since the templates only inject values directly into strings, validation is not affected. I therefore validated this code by copying it directly into JSHint.

Finally, the javascript that initialises the datepicker on the Add Workout page contains no jinja code, so I validated this code by copying it directly into JSHint.

| Script Location     |                                        Screenshot                                        |
|---------------------|:----------------------------------------------------------------------------------------:|
| script.js           |     ![](documentation/testing-images/javascript-validation/script-js-validation.jpg)     |
| track_progress.html | ![](documentation/testing-images/javascript-validation/track-progress-js-validation.jpg) |
| edit_workout.html   |  ![](documentation/testing-images/javascript-validation/edit-workout-js-validation.jpg)  |
| workout_log.html    |   ![](documentation/testing-images/javascript-validation/workout-log-js-validation.jpg)  |
| add_workout.html    |   ![](documentation/testing-images/javascript-validation/add-workout-js-validation.jpg)  |

The script.js code and the code on the add_workout page passed with no errors or warnings.

The track_progress code passed with two warnings: "One undefined variable - Chart" and "One unused variable - myChart". The undefined variable "Chart" is a chart object imported from chart.js and the unused variable "myChart" is used to initialise the chart on the page, so I don't consider the warnings to be an issue.

Finally, the edit_workout and workout_log code passed with warnings about the variable "M" being undefined. "M.Datepicker" refers to the Materialize datepickers and is defined in materialize.js.

### Python Validation

Validation of the app.py python file passed with no errors or warnings.

![app.py validation](documentation/testing-images/python-validation/python-validation.jpg)

***

## User Stories Testing
### Testing New User Stories

#### As a new user, I want to quickly understand the purpose of the site so that I can decide if it provides value to me.

* The welcome screen on the home page provides a brief overview of the purpose and features of the site to allow new users to quickly assess the value it offers.
* A link to the 'Getting Started' page is included in a prominent position on the welcome screen, which users can follow to find more in-depth information on the application.

![Welcome screen with overview and links](documentation/testing-images/user-stories/user-stories-1-1.jpg)

#### As a new user, I want to be able to quickly understand how to use the application to meet my needs.

* The 'Getting Started' page contains instructions on how to use the main application features.

![Instructions on the Getting Started page](documentation/testing-images/user-stories/user-stories-2-1.jpg)

* New users are redirected to this page upon registration of their account. The page is also linked from the Welcome Screen.

* The 'Getting Started' page links to the FAQ, where users can find more information if needed.

![Link to FAQ](documentation/testing-images/user-stories/user-stories-2-2.jpg)

* Both 'Getting Started' and 'FAQ' pages are linked from the nav bar for both logged in and logged out users.

![Logged in nav bar](documentation/testing-images/user-stories/user-stories-2-3.jpg)

![Logged out nav bar](documentation/testing-images/user-stories/user-stories-2-4.jpg)

#### As a new user, I want clear instructions on how to perform the featured exercises and record my progress.

* Detailed instructions on how to perform the exercises in the preset routines are included in the top accordion section of the FAQ page, which is open on page load.

![Exercise instructions on the FAQ page](documentation/testing-images/user-stories/user-stories-3-1.jpg)

* As well as written descriptions, the FAQ entry has a direct link to a YouTube search for videos showing proper form for each exercise. This is included as many people will find it easier to learn exercises by watching others perform them.

![Links to video searches](documentation/testing-images/user-stories/user-stories-3-2.jpg))

* Instructions for recording progress are included on the Getting Started page.
* The Workout Log and My Routines pages each have a box at the top of the page containing concise instructions for the features on that page.

![Information box on the Workout Log page](documentation/testing-images/user-stories/user-stories-3-3.jpg)

#### As a new user, I want to know where to look for more information and help if I don’t understand something.

* The instruction boxes on the Workout Log and My Routines pages both have links to the Getting Started guide and the FAQ.

* Links to the Getting Started guide and the FAQ are also provided in the nav bar.

### Testing Returning User Stories

#### As a returning user, I want to be able to quickly access the features I’m interested in.

* It's likely that returning users will usually be logging on to record a new workout, so users are redirected to the Workout Log page upon logging in. This page has a prominent "Add Workout Log" button at the top for adding workouts.

![Add Workout button at top of Workout Log page](documentation/testing-images/user-stories/user-stories-5-1.jpg)

* The nav bar provides quick access to all other features and pages of the site.

#### As a returning user, I want to be able to easily access and manage the data I’ve saved in the application.

* The Workout Log page provides access to all workouts recorded by users.
* Users can expand workout records to view key details and access the delete and edit options.

![Expanded workout log](documentation/testing-images/user-stories/user-stories-6-1.jpg)

* Edit workout log forms prepopulate with their current data for convenience

![Prepopulated edit form](documentation/testing-images/user-stories/user-stories-6-2.jpg)

* Workouts on the Workout log are displayed in batches of 10 and paginated so the page doesn't become too large to navigate easily

![Log pagination](documentation/testing-images/user-stories/user-stories-6-3.jpg)

* Users can filter the workout logs by date to help them find the records they're looking for

![Workout log filters](documentation/testing-images/user-stories/user-stories-6-4.jpg)

#### As a returning user, I want to be able to create and manage my own custom routines

* The My Routines page allows user to add their own routines

![Add routine button](documentation/testing-images/user-stories/user-stories-7-1.jpg)

* Routines can be edited or deleted using the buttons on the My Routines page

![Routine management buttons](documentation/testing-images/user-stories/user-stories-7-2.jpg)

* Edit routine forms prepopulate with their current data for convenience

#### As a returning user, I want to be able to assess my progress and whether the app is working for me

* Users can assess their progress on the track progress pages, which provide a helpful overview of stored data.

![Graph visualising progress](documentation/testing-images/user-stories/user-stories-8-1.jpg)

* The graphs provide a clear visualisation of how a user's scores are changing over time, which allows users to see if their fitness is improving by using the app.

#### As a returning user, I want to be able to share my achievements with others

* All user data is private by default, but users can opt to share their progress with a routine by clicking the "Share Page" button on the track progress pages.

![Share page button](documentation/testing-images/user-stories/user-stories-9-1.jpg)

* Once sharing is enabled for a page, users can send the page link to anyone to share their personal best score and progress graph.

![Share page link and hide page button](documentation/testing-images/user-stories/user-stories-9-2.jpg)

* Users can disable sharing by clicking the "Hide Page" button.

***

## Responsiveness Testing

Every page of the site was tested for responsiveness using the Firefox browser Responsive Design Mode and screen widths of 350px, 602px and 994px.

| Page            |                                 Mobile (350px)                                 |                                 Tablet (602px)                                 |                                 Desktop (994px)                                |
|-----------------|:------------------------------------------------------------------------------:|:------------------------------------------------------------------------------:|:------------------------------------------------------------------------------:|
| 404             |       ![](documentation/testing-images/responsiveness-tests/350-404.png)       |       ![](documentation/testing-images/responsiveness-tests/602-404.png)       |       ![](documentation/testing-images/responsiveness-tests/994-404.png)       |
| 500             |       ![](documentation/testing-images/responsiveness-tests/350-500.png)       |       ![](documentation/testing-images/responsiveness-tests/602-500.png)       |       ![](documentation/testing-images/responsiveness-tests/994-500.png)       |
| Add Routine     |   ![](documentation/testing-images/responsiveness-tests/350-add-routine.png)   |   ![](documentation/testing-images/responsiveness-tests/602-add-routine.png)   |   ![](documentation/testing-images/responsiveness-tests/994-add-routine.png)   |
| Add Workout     |   ![](documentation/testing-images/responsiveness-tests/350-add-workout.png)   |   ![](documentation/testing-images/responsiveness-tests/602-add-workout.png)   |   ![](documentation/testing-images/responsiveness-tests/994-add-workout.png)   |
| Edit Routine    |   ![](documentation/testing-images/responsiveness-tests/350-edit-routine.png)  |   ![](documentation/testing-images/responsiveness-tests/602-edit-routine.png)  |   ![](documentation/testing-images/responsiveness-tests/994-edit-routine.png)  |
| Edit Workout    |   ![](documentation/testing-images/responsiveness-tests/350-edit-workout.png)  |   ![](documentation/testing-images/responsiveness-tests/602-edit-workout.png)  |   ![](documentation/testing-images/responsiveness-tests/994-edit-workout.png)  |
| FAQ             |       ![](documentation/testing-images/responsiveness-tests/350-faq.png)       |       ![](documentation/testing-images/responsiveness-tests/602-faq.png)       |       ![](documentation/testing-images/responsiveness-tests/994-faq.png)       |
| Getting Started | ![](documentation/testing-images/responsiveness-tests/350-getting-started.png) | ![](documentation/testing-images/responsiveness-tests/602-getting-started.png) | ![](documentation/testing-images/responsiveness-tests/994-getting-started.png) |
| Home            |       ![](documentation/testing-images/responsiveness-tests/350-home.png)      |       ![](documentation/testing-images/responsiveness-tests/602-home.png)      |       ![](documentation/testing-images/responsiveness-tests/994-home.png)      |
| Login           |      ![](documentation/testing-images/responsiveness-tests/350-login.png)      |      ![](documentation/testing-images/responsiveness-tests/602-login.png)      |      ![](documentation/testing-images/responsiveness-tests/994-login.png)      |
| My Routines     |   ![](documentation/testing-images/responsiveness-tests/350-my-routines.png)   |   ![](documentation/testing-images/responsiveness-tests/602-my-routines.png)   |   ![](documentation/testing-images/responsiveness-tests/994-my-routines.png)   |
| Register        |     ![](documentation/testing-images/responsiveness-tests/350-register.png)    |     ![](documentation/testing-images/responsiveness-tests/602-register.png)    |     ![](documentation/testing-images/responsiveness-tests/994-register.png)    |
| Track Progress  |  ![](documentation/testing-images/responsiveness-tests/350-track-progress.png) |  ![](documentation/testing-images/responsiveness-tests/602-track-progress.png) |  ![](documentation/testing-images/responsiveness-tests/994-track-progress.png) |
| Workout Log     |   ![](documentation/testing-images/responsiveness-tests/350-workout-log.png)   |   ![](documentation/testing-images/responsiveness-tests/602-workout-log.png)   |   ![](documentation/testing-images/responsiveness-tests/994-workout-log.png)   |

***

## Compatibility Testing

Every page of the site was tested for compatibility with Google Chrome, Mozilla Firefox and Microsoft Edge. I wasn't able to test on Safari, as I didn't have access to any Apple devices with which to test.

![Testing with Google Chrome](documentation/testing-images/compatibility-tests/chrome-testing.jpg)

![Testing with Mozilla Firefox](documentation/testing-images/compatibility-tests/firefox-testing.jpg)

![Testing with Microsoft Edge](documentation/testing-images/compatibility-tests/edge-testing.jpg)

I created a checklist of tests to ensure all pages were rendering and functioning correctly and ran through the list on all browsers.

| Page            | Test                                     |       Chrome       |       Firefox      |        Edge        | Notes                                                        |
|-----------------|------------------------------------------|:------------------:|:------------------:|:------------------:|--------------------------------------------------------------|
| Home            | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Home            | All links working                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Register        | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Register        | All links working                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Register        | All form elements working                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Register        | Able to register account                 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Login           | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Login           | All links working                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Login           | All form elements working                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Login           | Able to login account                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Nav Bar         | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Nav Bar         | All links working                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Nav Bar         | Able to log out                          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Nav Bar         | Correct links showing when logged in/out | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Workout Log     | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Workout Log     | All links working                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Workout Log     | Accordions working                       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Workout Log     | Modals working                           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Workout Log     | Date filters working                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Workout Log     | Pagination working                       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Workout Log     | Able to delete logs                      | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Add Workout     | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | Edge responsive design mode bug found on this page           |
| Add Workout     | All form elements and pickers working    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Add Workout     | Able to add workout to database          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Edit Workout    | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Edit Workout    | Fields prepopulating correctly           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Edit Workout    | All form elements and pickers working    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Edit Workout    | Modals working                           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Edit Workout    | Able to push changes to database         | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| My Routines     | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| My Routines     | All links working                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| My Routines     | Add log preselection of routine working  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| My Routines     | Modals working                           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| My Routines     | Able to delete routines                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Add Routine     | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Add Routine     | All form elements and pickers working    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Add Routine     | Able to add routine to database          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Edit Routine    | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Edit Routine    | Fields prepopulating correctly           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Edit Routine    | All form elements and pickers working    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Edit Routine    | Modals working                           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Edit Routine    | Able to push changes to database         | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Track Progress  | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | Share link was overflowing from its parent element on Chrome |
| Track Progress  | Chart functioning                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Track Progress  | Modals working                           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Track Progress  | Able to update sharing setting           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Track Progress  | Able to view shared pages                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Track Progress  | Not able to view unshared pages          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Getting Started | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| Getting Started | All links working                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| FAQ             | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| FAQ             | All links working                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| FAQ             | Accordions working                       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| 404             | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| 404             | All links working                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| 500             | Responsive layout rendering correctly    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |
| 500             | All links working                        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |                                                              |

Only two issues were encountered during compatibility testing.

Firstly, an issue with Google Chrome where the sharing link generated on the Track Progress page was overflowing its parent container.

![Google Chrome overflowing link bug](documentation/testing-images/compatibility-tests/chrome-link-bug.jpg)

This was fixed by adding a .break-word utility class which applies the `word-wrap: break-word` property to the element:

![Google Chrome overflowing link bug fixed](documentation/testing-images/compatibility-tests/chrome-link-bug-fixed.jpg)

Secondly, there seemed to be an issue with some form pages being squeezed into too small a space on smaller screens on Microsoft Edge:

![Edge responsive bug](documentation/testing-images/compatibility-tests/edge-responsive-design-mode-bug-1.jpg)

However, on investigation it appears that this is actually a bug with Microsoft Edge's device emulation mode. The issue only occurred in the device emulation mode when a large window was dragged into a smaller window. Refreshing the page with the smaller window already set would fix the layout, and the issue didn't occur at all if a normal window (i.e. not using device emulation) was resized.

![Edge responsive bug 2](documentation/testing-images/compatibility-tests/edge-responsive-design-mode-bug-2.jpg)

***
## Bugs Fixed

### 1. An error was thrown if a user visited the logout page when already logged out

This was resolved by simply adding the @login_required decorator to the logout function, so logged out users cannot access the page.

### 2. When prepopulating the Edit Workout page with user data, the date and time were being added as full datetime strings

![Editworkout form showing full datetime](documentation/testing-images/bugs/bugs-2-datetime.jpg)

This was fixed by using the strftime() method within the jinja template to convert to the appropriate format for date and time:
```python
{{ log.date.strftime('%d/%m/%y') }}
{{ log.date.strftime('%H:%M') }}
```
### 3. Users could duplicate admin routine names

The code checked if a user had already used a routine name on form submission to prevent duplication, but didn't originally check if they were duplicating an admin routine. This could result in a confusing experience;

![Two routines with the same name](documentation/testing-images/bugs/bugs-3-duplicate-routine-names.jpg)

This was resolved by changing the database query that searched for duplicate names to use an $or expression:

```python
find_one(
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
```

### 4. The add and edit routine functions were storing "reps" as a string, instead of an int

Because of this, wherever the application tried to display total numbers of exercises by multiplying sets and reps, a long string of numbers was being printed.

![Total exercises being shows as a long string of 5s](documentation/testing-images/bugs/bugs-4-reps-as-strings.jpg)

This was resolved by converting the form input to an int on submission:
```python
"exercise_one_reps": int(request.form.get("exercise_one_reps"))
```

### 5. It was possible to enter 0 or negative numbers into the number of sets field when adding workout logs

![Negative number of sets in a workout log](documentation/testing-images/bugs/bugs-5-negative-sets.jpg)

This was resolved by simply adding min="1" to the HTML input elements.

### 6. An error was thrown when users visited the Track Progress page for a routine with no logs

![No records bug](documentation/testing-images/bugs/bugs-6-no-records.jpg)

This was resolved by adding a condition to the track_progress function that checks for logs. If no logs are found, users are redirected back to the my_routines page:
```python
if logs:
    # continue function
    # ...

flash("No workouts logged with this routine.", "error")
return redirect(url_for("my_routines"))
```

### 7. Track Progress Personal Best section wasn't displaying the earliest date

The 'Personal Best' section of the Track Progress page displays the date that the best score was achieved. When two scores were the same, however, it would display the first record added to the database, rather than the record with the earliest date, as would be preferred.

This happened because the personal best was being found with a $max database query, and the database was using the ObjectId as a tiebreaker (ObjectIds have a timestamp portion which represents the time the object was created). 

I resolved this by taking an alternative approach to finding the best score. Based on [this answer](https://stackoverflow.com/a/5326622) from StackOverflow, I used the python max() function on the list of logs that I'd already retrieved from the database earlier in the function, which was already sorted by date. I decided this was a preferable solution, as it saved a database query and avoided sorting by date twice.
```python
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

best = max(logs, key=lambda x: x['sets'])
```

### 8. An error was thrown if users entered invalid data into the date and time pickers

Although basic form validation was in place, it was possible for users to enter invalid data into the date and time pickers (e.g. an invalid date like the 30th of February), which would cause the application to throw an error.

![Invalid date entered](documentation/testing-images/bugs/bugs-8-invalid-date.jpg)

This was resolved by using a try-except block wherever the application converted user input into a datetime object, to handle the error gracefully:
```python
try:
    iso_date = datetime.datetime.strptime(date, "%d/%m/%y%H:%M")
except ValueError:
    flash(
        "Invalid date/time. Please enter a valid date and time in the "
        "formats dd/mm/yy and hh:mm.", "error")
    return redirect(url_for("add_workout"))
```

### 9. Search by date wasn't returning results for the last date entered

When a user entered a 'from' and 'to' date in the Workout Log filter form, any logs recorded on the 'to' date would not be shown. For example, if a user had a workout logged on 07/03/22 and they searched from 01/03/22 to 07/03/22, the workout would not be shown.

This happened because the search function was converting the entered 'from' and 'to' dates into datetime objects and then querying the database for records with a 'date' property greater than the 'from' date and less than the 'to' date:
```python
# convert input to datetime objects 
date_from = datetime.datetime.strptime(
                                request.args.get("date_from"), "%d/%m/%y")
date_to = datetime.datetime.strptime(
                                request.args.get("date_to"), "%d/%m/%y")

# find records between dates
"$match": {
    "username": session['user'],
    "date": {
        "$gte": date_from,
        "$lt": date_to
    }
}
```

Because only a date, and not a time, was being collected for both values, the time part of the datetime objects were defaulting to 00:00:00 - i.e. midnight at the beginning of the date entered. Therefore, any workouts logged after 00:00:00 on the 'to' date were outside the range of the query.

This was resolved by adding "23:59:59" to the date_to string before converting into a datetime object:
```python
date_to = datetime.datetime.strptime(
                                request.args.get("date_to") + "23:59:59",
                                "%d/%m/%y%H:%M:%S")
```

### 10. Mobile menu only visually hidden on larger screens

The mobile menu was visually hidden on larger screens, but remained in the document flow. This was fine for mouse navigation, as the element was simply invisible. 

However, it created a confusing experience for anyone navigating the site by keyboard, as the menu list items were still focusable. This meant that users were effectively forced to tab through the menu twice (once for the visible top nav and once for the invisible mobile nav) before reaching the page content.

This bug was resolved by simply adding the Materialize 'hide-on-large-screens-only' class to the mobile nav, which set the menu's display property to 'none', effectively removing it from the document flow.

### 11. My Routines page displaying the default routines twice for admin account

Because the My Routines page was set up to iterate through all admin added routines and then all routines added by the current user, when the current user was admin, the admin routines were added twice.

This bug was fixed by adding an if condition to the jinja template so that the first iteration wasn't run when admin was logged in:
```python
{% if session.user != "admin" %}
```

### 12. Window view returned to top of Workout Logs page when pagination controls used

When users clicked on "Older Logs" or "Newer Logs" to cycle through paginated records on the Workout Logs page, the window view would return to the top of the page. This created a frustrating user experience, as users would have to scroll down past the title, description and filters every time they changed page. 

This was resolved by adding an element id to the workout logs results section and adding that element to the older/newer pagination links. Now when the links are clicked, the user is taken directly to the results.

### 13. Entering invalid data into flask route parameters caused errors

The edit_workout, delete_workout, edit_routine, delete_routine, track_progress, and toggle_sharing pages all use route parameters to specify which records should be operated on. An error would be thrown if a user entered invalid data into these functions.

![Invalid object id entered in track_progress URL](documentation/testing-images/bugs/bugs-13-invalid-objectid.jpg)

![Invalid username entered in track_progress URL](documentation/testing-images/bugs/bugs-13-invalid-username.jpg)

This was fixed by adding code to each function to check if the data is valid. Submitted usernames are validated by querying the database and submitted log and routine ids are validated by using the ObjectId.is_valid() function. Users are redirected if invalid data is entered. e.g. from the track_progress function:
```python
# find the page owner in the users database
user = find_user(username)

# if username is not valid or routine id is not valid, redirect to
# my_routines
if not user or not ObjectId.is_valid(routine_id):
    flash("Invalid Username or Routine ID.", "error")
    return redirect(url_for("my_routines"))
```

### 14. Removing 'to_date' parameter from Workout Log URL caused an error

![Error caused by removing to_date from URL](documentation/testing-images/bugs/bugs-14-to_date-removed.jpg)

This happened because the code was only checking for a 'from_date' before executing code on the 'to_date', assuming a to_date would always be present. I resolved this by refactoring the code slightly and adding an 'and' condition to the if block to check that the to_date was present:
```python
# retrieve date_from and date_to values from query parameters if available
# and assign to variables
date_from = request.args.get("date_from")
date_to = request.args.get("date_to")
# if date_from and date_to query parameters were found
if date_from and date_to:
```

### 15. Error thrown if user entered an unmatching but valid Object Id into the URL

The edit_workout, delete_workout, edit_routine and delete_routine functions were checking if the variable in the URL was a valid object Id, but not if it matched any records. This meant that errors could be thrown if users entered an object id that was of a valid form, but not matching any documents in the database.

This was resolved for the edit_routine and delete_routine functions by adding error handling to the helper function that retrieves routines so an exception is raised if no record is found:
```python
if routine is None:
    raise ValueError('Invalid Routine Id')
```

Then adding a try except block to the edit_routine and delete_routine functions:
```python
try:
    routine = find_routine(routine_id)
except ValueError:
    flash("Invalid Routine ID.", "error")
    return redirect(url_for("my_routines"))
```

The bug was resolved for the edit_workout and delete_workout functions by adding a find_log helper function with the same functionality.

### 16. Messy generated HTML caused by poor white space control in jinja.

While validating the site code, I noticed that the layout of the HTML generated by my jinja templates was quite messy, with inconsistent indentation and many unnecessary empty lines.

I improved the layout of the generated HTML by using white space removal tags:
```python
# Strips all white space before and after the content block tags
{%- block content -%}
{%- endblock -%}
```
And indentation filters (based on [this answer](https://stackoverflow.com/a/53775887) on stackoverflow):

```python
# Indents all code between tags by 8 spaces
{% filter indent(width=8) %}
{% endfilter %}
```
There are still some areas with unnecessary empty lines which could be improved by a more thorough review of the code, but overall the generated HTML is much neater and easier to read now.

Home page generated source code before and after improving layout:

![Home page code before and after improving layout](documentation/testing-images/bugs/bugs-16-untidy-code.jpg)

### 17. Date picker popup using American date system when value prepopulated by jinja

Although the Materialize datepicker was configured to use the "dd/mm/yy" format, it would ignore this when the datepicker input field was prepopulated with a date and a user opened the datepicker popup. For example, the Edit Workout pages prepopulates the date of the workout being edited. In the screenshot below, the date of the edited workout is the first of June  or "01/06/22":

![Datepicker with prepopulated date](documentation/testing-images/bugs/bugs-17-datepicker-1.jpg)

If the user submits the form, the correct date will be submitted. However, if the user opens the datepicker to change the date, the datepicker will by default display dates in January, because it interprets the "01/06" as the sixth of January and so presents the user with other January dates:

![Incorrect month shown on datepicker](documentation/testing-images/bugs/bugs-17-datepicker-2.jpg)

This could be quite frustrating if a user only wanted to change the date by a day or two but had to scroll through multiple months to get there. The same issue was also present with the "from" and "to" date filters on the workout log page.

To fix this bug, I found it was necessary to set the desired date as the default date for each datepicker on initialisation. I found the [Materialize documentation](https://materializecss.com/pickers.html) and [this stack overflow thread](https://stackoverflow.com/questions/30324552/how-to-set-the-date-in-materialize-datepicker) helpful in understanding how to do this. I used jinja to inject the required date into a variable to use in the datepicker configuration:

```javascript
$(document).ready(function(){
    // convert log.date datetime into a string with the format "yyyy, mm, dd"
    let date = "{{ log.date.strftime('20%y') }}, {{ log.date.strftime('%m') }}, {{ log.date.strftime('%d') }}";

    // build an object to configure the date_from picker
    let options = {
    format: "dd/mm/yy",
    // set default date
    defaultDate: new Date(date),
    setDefaultDate: true
    };

    // find the datepicker
    let elems = $('.datepicker');

    // initialise the datepicker with the option  object
    M.Datepicker.init(elems[0], options);
});
```

With this code in place, the datepicker now shows the correct month and date when opened:

![Datepicker fixed](documentation/testing-images/bugs/bugs-17-datepicker-3.jpg)

I used the same technique to fix the datepickers on the Workout Logs page, though there it was necessary to initialise the two datepickers with two separate configurations and to add a jinja if / else block to handle the case where no dates are provided. 

It was also necessary to remove the datepicker initialisation code from the script.js file (where the other Materialize components are initialised) to prevent the datepickers from being initialised twice.

***

## Outstanding Issues

### 1. Accessibility Issues with Materialize select element

The Materialize select element works by hiding the actual select element and replacing it with an input field and unordered list, then using javascript to handle user selections.

Unfortunately, this creates an accessibility issue because the label that's applied to the select element is not transferred to the input field that's generated by Materialize. Technically, all form elements should have an appropriate label.

The input field is still functional, though, and can be fully navigated by keyboard. In my case, the default option that's active before a user selects an option reads "Select Routine", so this should provide an adequate description of the function of the input.

Given more development time, I would write some javascript to improve the accessibility of the Materialize select element, or replace it with a more accessible alternative. 

### 2. Untested on Safari

The site has not been tested on the Safari browser as I didn't have access to any Apple devices. I wouldn't anticipate any major compatibility issues, but I would need to do proper compatibility testing to be sure there were no bugs present. I would like to return to the project and do this testing at some point in the future when I have access to an Apple device to test with.

### 3. Internet Explorer Not Supported

The site doesn't support Internet Explorer and is unlikely to display or function correctly on this browser. I don't consider adding support for Internet Explorer to be a priority, as the browser is currently not widely used, is no longer updated, and is due to be retired in June 2022.