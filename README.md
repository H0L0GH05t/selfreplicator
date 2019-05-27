# Self-replicating App

A Django app, which replicates its own code into a GitHub repository, deployed on Heroku.
This app requires authentication from the user to access their public repositories. Once the user has accepted, the app will create a new public repository in their account. The repository will contain all of the basic files that comprise the app, and are required to run it locally.
In order to run this app 

## Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). 
```sh
$ git clone https://github.com/H0L0GH05t/selfreplicator.git
$ cd selfreplicator

$ python3 -m venv githubapps
$ pip install -r requirements.txt

$ createdb self_replicator

$ python manage.py migrate
$ python manage.py collectstatic

$ python migrate.py runserver
```

The app should now be running on [localhost:8000](http://localhost:8000/).

## Running on 

To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).


## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
