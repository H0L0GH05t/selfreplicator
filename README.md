# Self-replicating App

A Django app, which replicates its own code into a GitHub repository, created with Python using Django and deployed on Heroku.
This app requires authentication from the user to access their profile information and public repositories. Once the user has accepted, the app will create a new public repository in their account. The repository will contain all of the files required to run the app.

## How it Works

Clicking the replicate button sends a request to GitHub in the form of a url including the client ID assigned to this app after registering it with GitHub, and stating which places the app needs access to. For this app, access the user's GitHub profile and public repositories is what is required. It does not, however, require the users's password or access to the user's private repositories. A tab will be opened, displaying either GitHub's app authorization screen (if the user is already logged in) or a login screen, which will take the user to the app authorization screen upon logging in. If the user has already accepted access for this app, it will skip this part and immediately move to the next step.
Agreeing to accept the app's request for access sends the user to the callback url provided to GitHub when registering the app, which in this case should be the results page.
Along with the callback url, GitHub also adds a code to the end of the URL that can be exchanged for an authorization token, which allows the app to access the user's profile and public repositories.
This code is sent to GitHub's API in a request along with the app's client ID and client secret ID to exchange for an auth token that will temporarily allow the app access. The token is then used to get the authenticated user's username, so the correct url to the new repository is formed when pushing the app's files to it.
The repository is then created in the authenticated user's public repositories, using a request with the auth token, sending the name of the repository to be created, description, and an option telling it to not auto-initialize with a readme file, since we already have one in the project.
Then, for each file that will be copied from the app's files, a request is made with the auth token, the user's username, and the path to where the file should go.
Once the app has finished pushing each of the files to the newly created repository, it will load the results page. If everything has been completed successfuly, the results page should have a "Success" message and the log should show success for each step and file copied. If there was an error, the results page will have an "Error" message and display the cause of the error in the log. If the repository was created successfully, but there was a problem with copying one or more of the app's files to it, then a "Warning" message will be displayed, with the log showing the steps and files that succeeded, as well as identifying the files which failed.

## Requirements

In order to run this app, you will need to install Python 3.7 and a few libraries
When installing the app, the following libraries from requirements.txt will be installed:
- Python 3.7
- Django 2.2.1
- gunicorn 19.9.0
- django-heroku 0.3.1

These python libraries will also install their own required libraries, listed below:
- certifi 2019.3.9
- chardet 3.0.4
- dj-database-url 0.5.0
- idna 2.8
- psycopg2 2.8.2
- pytz 2019.1
- requests 2.22.0
- sqlparse 0.3.0
- urllib3 1.25.3
- whitenoise 4.1.2

To run the app from Heroku (as it is running here), you will also need:
- Postgres
- A Heroku account
- heroku-postgresql add on
- Heroku CLI
For more details, see How To Install.

## How To Install

Download the code from the GitHub repository created on your account and unzip it.
Create a new OAuth app on GitHub for this project here: https://github.com/settings/applications/new which will give you the necessary client IDs to connect to GitHub's API
Set the "Authorization callback URL" to the results page of the app. For example, "https://selfreplicator.herokuapp.com/results" (warning: if running locally on the dev server, this callback URL won't work correctly because the localhost is not a valid URL for this field)
Edit the setup_files.bat, and change the variables for client_id and client_secret to match the ones given by GitHub after registering the app.
Run setup_files.bat, and it will copy the Client ID and client Secret ID into the settings.py file in the githubapps folder, run python -m venv venv to create a python virtual environment folder in the project root, then pip install -r requirements.txt to install required python libraries.
To run the server, open a command prompt and navigate to the project root directory (where manage.py is located), then type python manage.py runserver to run the app using Django's development server. If you see the app's home page running on localhost:8000, that means you have correctly set up the app.
To deploy this app using Heroku you can check out their Getting Started guide: https://devcenter.heroku.com/articles/getting-started-with-python


## Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). 

python manage.py collectstatic
python manage.py runserver


The app should now be running on [localhost:8000](http://localhost:8000/).

## Deployed to Heroku

To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

git add .
git commit -m "commit message"
git push heroku master
