from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests
import os

def index(request):
    return render(request, "index.html")

def results(request):
    
    code_for_token = request.GET.get('code')

    auth_response = requests.post('https://github.com/login/oauth/access_token', params={'client_id':settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET, 'code': code_for_token}) #Accept: application/json
    if (auth_response.status_code != 200) or (auth_response.status_code !=201):
        return(request, "error.html", {'error_msg': "There was a problem with authentication"})
    access_token = auth_response.text.split('&')[0].replace('access_token=', '')
    
    username_response = requests.get('https://api.github.com/user', params={'access_token': access_token})
    if username_response.status_code != 200:
        return(request, "error.html", {'error_msg': "There was a problem with finding your profile"})
    username = username_response.json().get('login')
    
    create_repo(auth_token, username)
    
    return render(request, "results.html", {'client_id': settings.CLIENT_ID,
                                            'username': username})

# PUT /repos/:owner/:repo/contents/:path

def replicate_file(file_to_copy, username):
    file_to_copy = base64.b64encode(bytes(file_to_copy, 'utf-8'))
    contents_file = {'path': filepath,
                     'message':'replicated file',
                     'content': file_to_copy.decode("utf-8"),}
    requests.put('https://api.github.com/repos/%s/selfreplicatingapp/contents/%s' % (username, json.dumps(contents_file)))
    #response = requests.put('https://httpbin.org/put', data={'username': username, })

def create_repo(auth_token, username):
    
    # response = requests.post('https://api.github.com/user/repos', auth=(access_token), data=json.dumps(payload))
    response = requests.post('https://api.github.com/%s/repos' % username, data={'name': 'selfreplicatingapp',
                                                                                 'description': 'This is an app that creates a copy of itself as a repo on github.',
                                                                                 'homepage': 'selfreplicator.herokuapp.com',
                                                                                 'auto_init': False})
    
    # List of files to replicate
    appfiles = [
        'Procfile',                                  #gunicorn procfile
        'staticfiles',
        'Procfile.windows',                          # gunicorn for local windows
        'README.md',
        'requirements.txt',                          # list of all required libraries for python
        'runtime.txt',                               # version of python to use at runtime
        # 'db.sqlite3',                               # database file
        'selfreplicator',                            # app folder
        'selfreplicator/admin.py',
        'selfreplicator/__init__.py',
        'selfreplicator/apps.py',
        'selfreplicator/models.py',
        'selfreplicator/views.py',
        'selfreplicator/static',
        'selfreplicator/static/app-logo.png',
        'selfreplicator/static/selfreplicator.js',
        'selfreplicator/static/style.css',
        'selfreplicator/templates',                 # folder for html templates
        'selfreplicator/templates/results.html',
        'selfreplicator/templates/base.html',
        'selfreplicator/templates/index.html',
        'selfreplicator/templates/error.html',
        'githubapps',                               # Main site folder for project
        'githubapps/static',
        'githubapps/static/humans.txt',
        'githubapps/__init__.py',
        'githubapps/settings.py',
        'githubapps/urls.py',
        'githubapps/wsgi.py']
    
    for appfile in appfiles:
        #filepath relative from working directory (should be where manage.py is)
        with open(filepath) as f:
            file_to_copy = f.read()
            replicate_file(file_to_copy, username)
