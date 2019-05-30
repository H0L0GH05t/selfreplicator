from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests
import os
import json
import base64

def index(request):
    # add client id to the auth request link button
    return render(request, "index.html", {'client_id': settings.CLIENT_ID})

def results(request):
    
    # each step will report a status message to display in the log box in the results page
    result_msgs = []
    result_status = "error"
    
    # get the code to exchange for an access token
    code_for_token = request.GET.get('code')

    # exchange the code for an access token
    auth_response = requests.post('https://github.com/login/oauth/access_token', params={'client_id':settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET, 'code': code_for_token})
    if (auth_response.status_code == 200) or (auth_response.status_code == 201):
        result_msgs.append("Successfully obtained access token from GitHub")
        access_token = auth_response.text.split('&')[0].replace('access_token=', '')
            
        # create new repo in user's GitHub account
        result_status, result_msgs, new_repo_url = create_repo(access_token, result_msgs)
    else:
        # Record the authentication error message
        result_msgs.append("There was a problem with authentication - Response: %s" % auth_response.text)
        result_status = "error"
    
    #Select the correct results message to display
    error_result = "display:none;"
    warn_result = "display:none;"
    success_result = "display:none;"
    if result_status == "success":
        success_result = "display:block;"
    if result_status == "warning":
        warn_result = "display:block;"
    if result_status == "error":
        error_result = "display:block;"
    
    # render the results page with the status, aand link to user's new repo, and authorizations page
    return render(request, "results.html", {'client_id': settings.CLIENT_ID,
                                            'success_result': success_result,
                                            'warn_result': warn_result,
                                            'error_result': error_result,
                                            'results_msgs': result_msgs,
                                            'new_repo_url': new_repo_url})

# def get_authenticated_user(access_token):
def get_authenticated_user(headers, result_msgs, result_status):
    username = ''
    # get the authenticated user's username
    username_response = requests.get('https://api.github.com/user', headers=headers)
    if username_response.status_code == 200:
        username = username_response.json().get('login')
        result_msgs.append("Successfully found username %s from GitHub" % username)
        result_status = "success"
    else:
        # record the get user error message
        result_msgs.append("There was a problem with finding your profile: got status code %s" % username_response.status_code)
        result_status = "error"
    return username, result_msgs, result_status

def replicate_file(appfile, username, headers):
    
    # read in files as bytes then base64 encode for request and decode utf-8 for json
    with open(appfile, 'rb') as f:
        file_to_copy = f.read()
        
    content_file = base64.b64encode(file_to_copy).decode("utf-8")
        
    # add file to repo
    content_data = json.dumps({'path': appfile,
                               'message':'replicated file from app',
                               'content': content_file})
    create_file_response = requests.put('https://api.github.com/repos/%s/selfreplicatingapp/contents/%s' % (username, appfile), headers=headers, data=content_data)
    return create_file_response

def create_repo(access_token, result_msgs):    
    
    # create new repo in user's GitHub account
    headers = {'Authorization' : 'token %s' % access_token}
    data = {'name': 'selfreplicatingapp',
            'description': 'This is an app that creates a copy of itself as a repo on github.',
            'homepage': 'selfreplicator.herokuapp.com',
            'auto_init': False}
    create_repo_response = requests.post('https://api.github.com/user/repos', headers=headers, data=json.dumps(data))
    
    if create_repo_response.status_code == 201:
        result_status = "success"
        result_msgs.append("Successfully created new repo")
        
        # List of files in the app we need to replicate
        appfiles = ['Procfile',                                 #gunicorn procfile
                    'Procfile.windows',                         # gunicorn for local windows
                    'README.md',                                # github: documentation
                    'requirements.txt',                         # list of all required libraries for python
                    'runtime.txt',                              # version of python to use at runtime
                    'setup.bat',                                # Batch script to help set up this project for the first time
                    'SETUP.txt',                                # file containing client ids from github
                    '.gitignore',                               # gitignore for this project
                    'manage.py',                                # Django utility to run the app
                    'utils/setup_files.py',                     # utility script to create a settings.py file from the template containing the correct IDs
                    'selfreplicator/admin.py',                  # django: django admin page
                    'selfreplicator/__init__.py',               # django: generated init
                    'selfreplicator/apps.py',                   # django: generated app config
                    'selfreplicator/models.py',                 # django: model objects
                    'selfreplicator/views.py',                  # django: code each page view in urls
                    'selfreplicator/static/app-logo.png',       # custom logo
                    'selfreplicator/static/script.js',          # script for site
                    'selfreplicator/static/styles.css',         # styles for site
                    'selfreplicator/templates/base.html',       # contains the base html for the site
                    'selfreplicator/templates/index.html',      # home page
                    'selfreplicator/templates/results.html',    # will show results message
                    'selfreplicator/templates/404.html',        # custom 404 page
                    'selfreplicator/templates/403.html',        # custom 403 page
                    'selfreplicator/templates/500.html',        # custom 500 page
                    'githubapps/__init__.py',                   # django: generated init file
                    'githubapps/settings-template.py',          # django: settings for project
                    'githubapps/urls.py',                       # django: url paths to use
                    'githubapps/wsgi.py']                       # django: wsgi settings for app
        
        # get username so we can push files to the new repo
        username, result_msgs, result_status = get_authenticated_user(headers, result_msgs, result_status)
        
        # push each file to the repo
        for appfile in appfiles:
            if os.path.exists(appfile):
                create_file_response = replicate_file(appfile, username, headers)
                result_msgs.append("Copy file: %s -- %s" % (appfile, ("success" if create_file_response.status_code == 201 else "failed: %s" % create_file_response.text)))
            else:
                # Record the file that failed to be created in the repo
                result_msgs.append("!! Missing file: %s" % appfile)
                result_status = "warning"
        
    else:
        # record repo creation error message
        result_msgs.append("Failed to create new repo in user's GitHub account - Response: %s" % create_repo_response.text)
        result_status = "error"
        
    new_repo_url = ""
    if result_status != "error":
        # If there were no errors creating the repo, set up the URL for the button
        new_repo_url = "https://github.com/%s/selfreplicatingapp" % username
            
    return result_status, result_msgs, new_repo_url
