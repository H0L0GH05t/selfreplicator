from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests

def index(request):
    return render(request, "index.html")

def results(request):
    response = requests.get('https://github.com/login/oauth/authorize',
                            params={'client_id':'c66f4b201302de0cfe4e&',
                                    'scope': 'user public_repo write:repo_hook'})
    
    code_for_token = response.text.replace('/results/?code=','')
    
    # GET '/results/?code=3c4b7539b00cacfa9dc8'
    auth_response = requests.post('https://github.com/login/oauth/access_token', params={'client_id':settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET, 'code': code_for_token}) #Accept: application/json
    access_token='not found'
    try:
        if auth_response.access_token:
            access_token = auth_response.access_token
    except:
        access_token = access_token.split('&')[0]
        pass
    # request.get_full_path
    username = 'not found'
    username_response = requests.get('https://api.github.com/user', params={'access_token': access_token})
    test = 'failed'
    try:
        if username_response.login:
            username = username_response.login
            test = 'not necessary'
    except:
        test = username_response
        pass
    
    # ("https://api.github.com/users/<username>/repos?access_token=<generated token>"
    return render(request, "results.html", {'access_token': access_token,
                                            'client_id': settings.CLIENT_ID,
                                            'username': username,
                                            'code_for_token' : code_for_token,
                                            'test': test})

# GET /repos/:owner/:repo/contents/
# PUT /repos/:owner/:repo/contents/:path

def create_repo(filepath, auth_token, repo):
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
            
        file_to_copy = base64.b64encode(bytes(file_to_copy, 'utf-8'))
        contents_file = {'path': filepath, 'message':'including file', 'content': file_to_copy.decode("utf-8")}
        requests.put('https://api.github.com/repos/%s/%s/contents/%s' % (username, repo, json.dumps(contents_file)))
    payload = {'name': repo, 'description': 'this is a self-replication app.', 'auto_init': False}
    login = requests.post('https://api.github.com/user/repos', auth=(access_token), data=json.dumps(payload))

    if login.status_code == 201:
        return jsonify({'success' : 'Repo is replicated', 'user' : username})
    return jsonify({'error' : login.json()['message']})