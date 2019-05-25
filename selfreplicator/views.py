from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests
import os
import json
import base64

def index(request):
    return render(request, "index.html")

def results(request):
    
    result_msgs = []
    result_status = "success" #TODO: make this an int
    created_repo_link = ""
    # get the code to exchange for an access token
    code_for_token = request.GET.get('code')

    # exchange the code for an access token
    auth_response = requests.post('https://github.com/login/oauth/access_token', params={'client_id':settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET, 'code': code_for_token})
    if (auth_response.status_code == 200) or (auth_response.status_code == 201):
        result_msgs.append("Successfully obtained access token from GitHub")
        # access_token = auth_response.json('access_token')
        access_token = auth_response.text.split('&')[0].replace('access_token=', '')
            
        # create new repo in user's GitHub account
        result_status, result_msgs, created_repo_link = create_repo(access_token, result_msgs)
            
    else:
         # Record the authentication error message
        result_msgs.append("There was a problem with authentication - Response: %s" % auth_response.text)
        result_status = "error"
    
    # render the results page with the status, and link to user's authorization for this app
    return render(request, "results.html", {'client_id': settings.CLIENT_ID,
                                            'result_status': result_status,
                                            'results_msgs': result_msgs,
                                            'created_repo_link': created_repo_link,})
def file_is_text(filename):
    if '.' in filename:
        exts = ['json',
                'py',
                'txt',
                'md',
                'windows',
                'html',
                'css',
                'js']
        file_ext = filename.rsplit('.',1)[1]
        if file_ext in image_ext:
            return True
    return False

# def get_authenticated_user(access_token):
def get_authenticated_user(headers, result_msgs, result_status):
    username = ''
    # get the authenticated user's username
    username_response = requests.get('https://api.github.com/user', headers=headers)
    # username_response = requests.get('https://api.github.com/user', params={'access_token': access_token})
    if username_response.status_code == 200:
        username = username_response.json().get('login')
        result_msgs.append("Successfully found user profile %s from GitHub" % username)
    else:
        # record the get user error message
        result_msgs.append("There was a problem with finding your profile: got status code %s" % username_response.status_code)
        result_status = "error"
    return username, result_msgs, result_status

def replicate_file(appfile, username, headers):
    
    # open files (not dirs)
    with open(appfile) as f:
            file_to_copy = f.read()
            
    if file_is_text(appfile):
        # only utf-8 decode text files
        content_file = base64.b64encode(bytes(file_to_copy, 'utf-8')).decode("utf-8")
    elif '.' in appfile:
        content_file = base64.b64encode(bytes(file_to_copy, 'utf-8'))
    else:
        content_file = file_to_copy
        
    # add file to repo
    content_data = json.dumps({'path': appfile,
                     'message':'replicated file from app',
                     'content': content_file})
    create_file_response = requests.put('https://api.github.com/repos/%s/selfreplicatingapp/contents/%s' % (username, appfile), headers=headers, data=content_data)
    return create_file_response

def create_repo(access_token, result_msgs):    
    created_repo_link = ''
    # create new repo in user's GitHub account
    headers = {'Authorization' : 'token %s' % access_token}
    data = {'name': 'selfreplicatingapp',
            'description': 'This is an app that creates a copy of itself as a repo on github.',
            'homepage': 'selfreplicator.herokuapp.com',
            'auto_init': False}
    create_repo_response = requests.post('https://api.github.com/user/repos', headers=headers, data=json.dumps(data))
    if create_repo_response.status_code == 201:
        result_status = "success"
        result_msgs.append("successfully created new repo")
        
        # List of files in the app we need to replicate
        appfiles = ['Procfile',                                 #gunicorn procfile
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
                    'selfreplicator/static/selfreplicator.js',  # script for site
                    'selfreplicator/static/selfreplicator.css', # styles for site
                    'selfreplicator/templates',                 # folder for html django templates
                    'selfreplicator/templates/base.html',       # contains the base html for the site
                    'selfreplicator/templates/index.html',      # home page
                    'selfreplicator/templates/results.html',    # will show results message
                    'githubapps',                               # django project root folder
                    'githubapps/static',                        # empty static dir
                    'githubapps/static/humans.txt',             # blank file so dir is not empty
                    'githubapps/__init__.py',                   # django: generated init file
                    'githubapps/settings.py',                   # django: settings for project
                    'githubapps/urls.py',                       # django: url paths to use
                    'githubapps/wsgi.py']                       # django: wsgi settings for app
        
        # get username so we can push files to the new repo
        username, result_msgs, result_status = get_authenticated_user(headers, result_msgs, result_status)
        created_repo_link = "https://github.com/%s/selfreplicatingapp" % username
        
        for appfile in appfiles:
            if os.path.exists(appfile):
                create_file_response = replicate_file(appfile, username, headers)
                result_msgs.append("Copy file: %s -- %s" % (appfile, ("success" if create_file_response.status_code == 201 else "failed: %s" % create_file_response.text)))
            else:
                result_msgs.append("!! Missing file: %s" % appfile)
        
    else:
        # record repo creation error message
        result_status = "error"
        result_msgs.append("Failed to create new repo in user's GitHub account - Response: %s" % create_repo_response.text)
            
    return result_status, result_msgs, created_repo_link
