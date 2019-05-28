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
    result_status = "error"
    # get the code to exchange for an access token
    code_for_token = request.GET.get('code')

    # exchange the code for an access token
    auth_response = requests.post('https://github.com/login/oauth/access_token', params={'client_id':settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET, 'code': code_for_token})
    if (auth_response.status_code == 200) or (auth_response.status_code == 201):
        result_msgs.append("Successfully obtained access token from GitHub")
        access_token = auth_response.text.split('&')[0].replace('access_token=', '')
            
        # create new repo in user's GitHub account
        result_status, result_msgs = create_repo(access_token, result_msgs)
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
    
    # render the results page with the status, and link to user's authorization for this app
    return render(request, "results.html", {'client_id': settings.CLIENT_ID,
                                            'success_result': success_result,
                                            'warn_result': warn_result,
                                            'error_result': error_result,
                                            'results_msgs': result_msgs,})

# def get_authenticated_user(access_token):
def get_authenticated_user(headers, result_msgs, result_status):
    username = ''
    # get the authenticated user's username
    username_response = requests.get('https://api.github.com/user', headers=headers)
    # username_response = requests.get('https://api.github.com/user', params={'access_token': access_token})
    if username_response.status_code == 200:
        username = username_response.json().get('login')
        result_msgs.append("Successfully found user profile %s from GitHub" % username)
        result_status = "success"
    else:
        # record the get user error message
        result_msgs.append("There was a problem with finding your profile: got status code %s" % username_response.status_code)
        result_status = "error"
    return username, result_msgs, result_status

def replicate_file(appfile, username, headers):
    
    if '.' in appfile:
        with open(appfile, 'rb') as f:
            file_to_copy = f.read()
    else:
        file_to_copy = bytes(appfile, 'utf-8')
        
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
                    # 'db.sqlite3',                             # database file
                    'setup.bat',                                # Batch script to help set up this project for the first time
                    'utils/setup_files.py'                      # utility script to create a settings.py file from the template containing the correct IDs
                    'selfreplicator/admin.py',                  # django: django admin page
                    'selfreplicator/__init__.py',               # django: generated init
                    'selfreplicator/apps.py',                   # django: generated app config
                    'selfreplicator/models.py',                 # django: model objects
                    'selfreplicator/views.py',                  # django: code each page view in urls
                    'selfreplicator/static/app-logo.png',       # custom logo
                    'selfreplicator/static/script.js',  # script for site
                    'selfreplicator/static/styles.css', # styles for site
                    'selfreplicator/templates/base.html',       # contains the base html for the site
                    'selfreplicator/templates/index.html',      # home page
                    'selfreplicator/templates/results.html',    # will show results message
                    'githubapps/static/humans.txt',             # blank file so dir is not empty
                    'githubapps/__init__.py',                   # django: generated init file
                    'githubapps/settings-template.py',          # django: settings for project
                    'githubapps/urls.py',                       # django: url paths to use
                    'githubapps/wsgi.py']                       # django: wsgi settings for app
        
        # get username so we can push files to the new repo
        username, result_msgs, result_status = get_authenticated_user(headers, result_msgs, result_status)
        
        for appfile in appfiles:
            if os.path.exists(appfile):
                create_file_response = replicate_file(appfile, username, headers)
                result_msgs.append("Copy file: %s -- %s" % (appfile, ("success" if create_file_response.status_code == 201 else "failed: %s" % create_file_response.text)))
            else:
                result_msgs.append("!! Missing file: %s" % appfile)
                result_status = "warning"
        
    else:
        # record repo creation error message
        result_msgs.append("Failed to create new repo in user's GitHub account - Response: %s" % create_repo_response.text)
        result_status = "error"
            
    return result_status, result_msgs

# Custom error pages

# def handler404(request, exception, template_name="error.html"):
#     response = render_to_response("error.html", {'error_msg': exception,
#                                                  'test': request})
#     response.status_code = 404
#     return response
# 
# def handler500(request, exception, template_name="500.html"):
#     response = render_to_response("500.html", {'error_msg': exception,
#                                                  'test': request})
#     response.status_code = 500
#     return response
# 
# def handler403(request, exception, template_name="403.html"):
#     response = render_to_response("403.html", {'error_msg': exception,
#                                                  'test': request})
#     response.status_code = 403
#     return response
