from django.shortcuts import render
from django.http import HttpResponse
import requests

def getGitHubAuth(request):
    access_token = {}
    url = 'https://github.com/login/oauth/authorize?client_id=c66f4b201302de0cfe4e& scope=user%20public_repo write:repo_hook read:repo_hook redirect_uri=http://localhost:8000/results'
    response = requests.get(url)
    access_token = response.json()
    return render(request, 'results.html', {'access_token': access_token})

def index(request):
    return render(request, "index.html")

def results(request):
    test = request.get_full_path
    access_token = 'not found'
    if 'access_token' in request.POST:
        access_token = request.POST['access_token']
    return render(request, "results.html", {'access_token': access_token, 'test' : test})

# GET /repos/:owner/:repo/contents/
# PUT /repos/:owner/:repo/contents/:path

# example commit:
# {
#   "message": "my commit message",
#   "committer": {
#     "name": "Scott Chacon",
#     "email": "schacon@gmail.com"
#   },
#   "content": "bXkgbmV3IGZpbGUgY29udGVudHM="
# }

# git config --global user.name "John Smith"
# git remote add beanstalk git@accountname.beanstalkapp.com:/gitreponame.git
# git push beanstalk
# "https://github.com/login/oauth/authorize?client_id=c66f4b201302de0cfe4e& scope=user%20public_repo write:repo_hook read:repo_hook"

# def 


def create_repo():
    with open(path) as f:
        filename = f.read()
        
    filename = base64.b64encode(bytes(filename, 'utf-8'))
    file = {'path': path, 'message':'add {}'.format(path), 'content': filename.decode("utf-8")}
    requests.put('https://api.github.com/repos/%s/%s/contents/%s' % (user, repo, json.dumps(file)))
    
    # List of files to replicate
    FILES = [
        'replication.py',
        '.flaskenv',
        'Procfile',
        'wakeup.py',
        '.gitattributes',
        'README.md',
        'installation.md',
        'tech_specs.md',
        'app/routes.py',
        'app/__init__.py',
        'app/static/css/style.css',
        'app/static/js/script.js',
        'app/templates/index.html'
    ]
    
    # for file in FILES: # instead of this we want to do a git pull?
    #     create_file(file, user, password, repo)
    payload = {'name': repo, 'description': 'this is a self-replication app.', 'auto_init': False}
    login = requests.post('https://api.github.com/user/repos', auth=(user, password), data=json.dumps(payload))

    if login.status_code == 201:
        return jsonify({'success' : 'Repo is replicated', 'user' : user})
    return jsonify({'error' : login.json()['message']})