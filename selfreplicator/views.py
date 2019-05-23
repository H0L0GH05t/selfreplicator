from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests
import os

def index(request):
    return render(request, "index.html")

def results(request):
    # get the code to exchange for an access token
    code_for_token = request.GET.get('code')

    # exchange the code for an access token
    auth_response = requests.post('https://github.com/login/oauth/access_token', params={'client_id':settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET, 'code': code_for_token})
    if (auth_response.status_code != 200) or (auth_response.status_code !=201):
        return(request, "error.html", {'error_msg': "There was a problem with authentication"})
    access_token = auth_response.text.split('&')[0].replace('access_token=', '')
    
    # get the authenticated user's username
    username_response = requests.get('https://api.github.com/user', params={'access_token': access_token})
    if username_response.status_code != 200:
        return(request, "error.html", {'error_msg': "There was a problem with finding your profile"})
    username = username_response.json().get('login')
    
    # create the new repo and push the app files to it
    create_repo(auth_token, username)
    
    # render the results page with the status, and link to user's authorization for this app
    return render(request, "results.html", {'client_id': settings.CLIENT_ID,
                                            'username': username})

def replicate_file(file_to_copy, username):
    
    # encode file to be pushed to repo
    file_to_copy = base64.b64encode(bytes(file_to_copy, 'utf-8'))
    # set up content to 
    contents_file = {'path': filepath,
                     'message':'replicated file',
                     'content': file_to_copy.decode("utf-8"),}
    requests.put('https://api.github.com/repos/%s/selfreplicatingapp/contents/%s' % (username, json.dumps(contents_file)))
    #response = requests.put('https://httpbin.org/put', data={'username': username, })

def create_repo(auth_token, username):
    # create new repo in user's GitHub account
    #response = requests.post('https://api.github.com/user/repos', data=data, auth=(username, access_token))
    response = requests.post('https://api.github.com/%s/repos' % username, data={'name': 'selfreplicatingapp',
                                                                                 'description': 'This is an app that creates a copy of itself as a repo on github.',
                                                                                 'homepage': 'selfreplicator.herokuapp.com',
                                                                                 'auto_init': False})
    
    # List of files to replicate
    appfiles = [
        'Procfile',                                 #gunicorn procfile
        'staticfiles',                              # empty dir to collect static with whitenoise
        'Procfile.windows',                         # gunicorn for local windows
        'README.md',                                # github: documentation
        'requirements.txt',                         # list of all required libraries for python
        'runtime.txt',                              # version of python to use at runtime
        # 'db.sqlite3',                             # database file
        'selfreplicator',                           # django app root folder
        'selfreplicator/admin.py',                  # django: django admin page
        'selfreplicator/__init__.py',               # django: generated init
        'selfreplicator/apps.py',                   # django: generated app config
        'selfreplicator/models.py',                 # django: model objects
        'selfreplicator/views.py',                  # django: code each page view in urls
        'selfreplicator/static',                    # static file location
        'selfreplicator/static/app-logo.png',       # custom logo
        'selfreplicator/static/selfreplicator.js',  # script for entire site
        'selfreplicator/static/style.css',          # styles for entire site
        'selfreplicator/templates',                 # folder for html django templates
        'selfreplicator/templates/base.html',       # contains the base html for the site
        'selfreplicator/templates/index.html',      # home page
        'selfreplicator/templates/results.html',    # will show results of replication
        'selfreplicator/templates/error.html',      # rendered when replication fails due to error
        'githubapps',                               # django project root folder
        'githubapps/static',                        # empty static dir
        'githubapps/static/humans.txt',             # blank file so dir is not empty
        'githubapps/__init__.py',                   # django: generated init file
        'githubapps/settings.py',                   # django: settings for project
        'githubapps/urls.py',                       # django: url paths to use
        'githubapps/wsgi.py']                       # django: wsgi settings for app
    
    for appfile in appfiles:
        # filepath relative from working dir (should be where manage.py is)
        # open file we need to copy to repo and call replicate file
        with open(filepath) as f:
            file_to_copy = f.read()
            replicate_file(file_to_copy, username)
