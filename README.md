# Self-replicating App

A Django app, which replicates its own code into a GitHub repository, created with Python using Django and deployed on Render.
This app requires authentication from the user to access their profile information and public repositories. Once the user has accepted, the app will create a new public repository in their account. The repository will contain all of the files required to run the app.

## How it Works

This application was created with Python using Django and deployed on Render.

Clicking the replicate button sends a request to GitHub in the form of a url including the client ID assigned to this app after registering it with GitHub, and stating which places the app needs access to. For this app, access the user's public repositories is what is required. It does not, however, require the users's password or access to the user's private repositories. A tab will be opened, displaying either GitHub's app authorization screen (if the user is already logged in) or a login screen, which will take the user to the app authorization screen upon logging in. If the user has already accepted access for this app, it will skip this part and immediately move to the next step. Agreeing to accept the app's request for access sends the user to the callback url provided to GitHub when registering the app, which in this case should be the results page.
Along with the callback URL, GitHub also adds a code to the end of the URL that is necessary to exchange for an authorization token, which allows the app to use the permission granted by the user to access their profile and public repositories. This code is sent to GitHub's API in a request along with the app's client ID and client secret ID to exchange for an auth token that will temporarily allow the app access. The token is then used to get the authenticated user's username, so the correct url to the new repository is formed when pushing the app's files to it.
Using a request containing the auth token, the name of the repository to be created, description, and an option telling it to not auto-initialize with a readme file (since we already have one in the project), the new repository is created in the authenticated user's public repositories. Then, for each file that will be copied from the app's files, a request is made with the auth token, the user's username, and the path to where the file should go. Once the app has finished pushing each of the files to the newly created repository, it will load the results page. If everything has been completed successfuly, the results page should have a "Success" message and the log should show success for each step and file copied. If there was an error, the results page will have an "Error" message and display the cause of the error in the log. If the repository was created successfully, but there was a problem with copying one or more of the app's files to it, then a "Warning" message will be displayed, with the log showing the steps and files that succeeded, as well as identifying the files which failed.

## Requirements

In order to run this app, you will first need to install Python 3.7 and a few libraries.
When installing the app, the following libraries from requirements.txt will be installed:

- Django 2.2.13
- gunicorn 19.9.0
- requests 2.22.0

These python libraries will also install their own required libraries, listed below:

- certifi 2019.3.9
- chardet 3.0.4
- dj-database-url 0.5.0
- idna 2.8
- psycopg 2 2.8.2
- pytz 2019.1
- sqlparse 0.3.0
- urllib3 1.25.3
- whitenoise 4.1.2

To run the app from Render (as it is running here), you will also need:

- Git
- A Render account
- A GitHub account

For more details, see How To Install.

## How To Install

Set up and deploying to Render:

- Install Python 3.7 from the [download page here](https://www.python.org/downloads/release/python-373/).
- You will also need to [download and install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) if you do not already have it.
- To set up git for the first time follow the instructions [in this guide](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup).
- Download the zip containing the app's code from the GitHub repository and unzip it, or clone it locally with git.
- Open a command prompt in the project root directory (inside selfreplicatingapp-master) and type git init to turn this project into a git repository.
- Next, you will need to [create a free Render account](https://www.render.com") and connect it to GitHub.
- Navigate to render's website and select the new button and create a new Web Service.
- Connect to the GitHub repository from your own account, or via the project's public url.
- Set the name for your web service, this will be used for the url as well.
- Select the branch of the repository to use, in most cases it will be 'main'.
- Runtime should be Python 3.
- For the Start Command, add "gunicorn githubapps.wsgi".
- The Build Command should be "pip install -r requirements.txt"
- Once set up, you should be able to deploy by clicking the manual deploy button.
- Congratulations! The app is now deployed and can be seen using its URL.

- In order to set this up from your own repository copy there's a few more steps to follow.
- Next we need to get the necessary client IDs to connect to GitHub's API. To do this, follow the prompts to create a new OAuth app on GitHub for this project [here](https://github.com/settings/applications/new).
- The homepage URL should be the domain provided by render which appears on the dashboard for your web service, for example: "https://my-app-name.onrender.com". Set the "Authorization callback URL" to the results page of the app. For example, "https://my-app-name.onrender.com/results". Hit the button to register this app and you'll be taken to the app's info screen.
- Edit the SETUP.txt file in the root folder of the project by copying and pasting the values for "client_id" and "client_secret" from the app info page on GitHub into the labeled spots, then save and close the file.
- Open a command prompt this same folder and type setup.bat to run the batch file. It will run python -m venv venv to create a python virtual environment. folder in the project root, then pip install -r requirements.txt to install required python libraries. It will also read the Client ID and Client Secret ID you copied to the SETUP.txt file, generate a Secret ID, and paste these values into the settings.py file in the githubapps folder. 
- Now that it has been created and set up, you can deploy it by typing git push master.
- On render, you can now manually deploy again for the latest commit to your repository if it does not automatically redeploy.


To run the app Locally:

- Type python manage.py collectstatic into the command prompt. This will collect all the static files so that they can be served correctly while running locally.
- Type python manage.py runserver into the command prompt. This should start the built-in django server for running locally.
- Open your web browser to http://localhost:5000">http://localhost:5000). You should see your app running locally.
- To stop the app from running locally, go back to your command prompt window and press Ctrl+C to exit.
