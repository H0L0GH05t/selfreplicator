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
    
    # List of files in the app we need to replicate
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
        'selfreplicator/templates/results.html',    # will show results message
        'githubapps',                               # django project root folder
        'githubapps/static',                        # empty static dir
        'githubapps/static/humans.txt',             # blank file so dir is not empty
        'githubapps/__init__.py',                   # django: generated init file
        'githubapps/settings.py',                   # django: settings for project
        'githubapps/urls.py',                       # django: url paths to use
        'githubapps/wsgi.py']                       # django: wsgi settings for app
    
    username = "Not found"
    result_msgs = []
    result_status = "success" #TODO: make this an int
    created_repo_link = ""
    test = 'TEST' #TODO: remove
    # get the code to exchange for an access token
    code_for_token = request.GET.get('code')

    # exchange the code for an access token
    auth_response = requests.post('https://github.com/login/oauth/access_token', params={'client_id':settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET, 'code': code_for_token})
    if (auth_response.status_code == 200) or (auth_response.status_code == 201):
        result_msgs.append("Successfully obtained access token from GitHub")
        # access_token = auth_response.json('access_token')
        access_token = auth_response.text.split('&')[0].replace('access_token=', '')
            
        # create new repo in user's GitHub account
        headers = {'Authorization' : 'token %s' % access_token}
        data = {'name': 'selfreplicatingapp',
                'description': 'This is an app that creates a copy of itself as a repo on github.',
                'homepage': 'selfreplicator.herokuapp.com',
                'auto_init': False}
        create_repo_response = requests.post('https://api.github.com/user/repos', headers=headers, data=json.dumps(data))
        test = create_repo_response.json().get('location')
        if create_repo_response.status_code == 201:
            result_status = "success"
            result_msgs.append("successfully created new repo")
            # created_repo_link = create_repo_response.json().get('location')
            
            for appfile in appfiles:
                if os.path.exists(appfile):
                    result_msgs.append("found file: %s" % appfile)
            result_msgs.append("finished file verification")
                    
            
        else:
            # record repo creation error message
            result_status = "error"
            result_msgs.append("Failed to create new repo in user's GitHub account - Response: %s" % create_repo_response.text)
            
    else:
         # Record the authentication error message
        result_msgs.append("There was a problem with authentication - Response: %s" % auth_response.text)
        result_status = "error"
        
        # try:
        # create the new repo and push the app files to it
        #   result_status, result_msgs, created_repo_link, result_status = create_repo(auth_token, username, result_msgs)
        # except:
        #     result_status = "error"
        #     result_msgs.append("Failed to create repo in user %s's public repos" % username)
    
    # render the results page with the status, and link to user's authorization for this app
    return render(request, "results.html", {'client_id': settings.CLIENT_ID,
                                            'result_status': result_status,
                                            'results_msgs': result_msgs,
                                            'created_repo_link': created_repo_link,
                                            'code': test})

# def get_authenticated_user(access_token):
def get_authenticated_user(headers):
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
    return username

def replicate_file(file_to_copy, username):
    
    # encode file to be pushed to repo
    file_to_copy = base64.b64encode(bytes(file_to_copy, 'utf-8'))
    # set up content to 
    contents_file = {'path': filepath,
                     'message':'replicated file',
                     'content': file_to_copy.decode("utf-8"),}
    requests.put('https://api.github.com/repos/%s/selfreplicatingapp/contents/%s' % (username, json.dumps(contents_file)))

def create_repo(auth_token, result_msgs):    
    created_repo_link = ''
    # create new repo in user's GitHub account
    headers = {'Authorization' : 'token %s' % access_token}
    data = {'name': 'selfreplicatingapp',
            'description': 'This is an app that creates a copy of itself as a repo on github.',
            'homepage': 'selfreplicator.herokuapp.com',
            'auto_init': False}
    create_repo_response = requests.post('https://api.github.com/user/repos', headers=headers, data=json.dumps(data))
    test = create_repo_response.json().get('location')
    if create_repo_response.status_code == 201:
        result_status = "success"
        result_msgs.append("successfully created new repo")
        # created_repo_link = create_repo_response.location
        
        # get username so we can push files to the new repo
        username = get_authenticated_user(headers)
        
        for appfile in appfiles:
            if os.path.exists(appfile):
                result_msgs.append("found file: %s" % appfile)
        result_msgs.append("finished file verification")
        
        
        replicate_file(appfile, username)
                
        
    else:
        # record repo creation error message
        result_status = "error"
        result_msgs.append("Failed to create new repo in user's GitHub account - Response: %s" % create_repo_response.text)
            
    return result_status, result_msgs, created_repo_link, response.status_code
