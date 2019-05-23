from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests
import os

def index(request):
    return render(request, "index.html")

def results(request):
    
    username = "Not found"
    result_msgs = []
    result_status = "success"
    created_repo_link = ""
    
    # get the code to exchange for an access token
    code_for_token = request.GET.get('code')

    # exchange the code for an access token
    auth_response = requests.post('https://github.com/login/oauth/access_token', params={'client_id':settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET, 'code': code_for_token})
    if (auth_response.status_code == 200) or (auth_response.status_code == 201):
        result_msgs.append("Successfully obtained access token from GitHub")
        access_token = auth_response.text.split('&')[0].replace('access_token=', '')
        
        # get the authenticated user's username
        username_response = requests.get('https://api.github.com/user', params={'access_token': access_token})
        if username_response.status_code == 200:
            username = username_response.json().get('login')
            result_msgs.append("Successfully found user profile %s from GitHub" % username)
        else:
            # record the user error message
            # results_msg = "There was a problem with finding your profile: got status code %s" % username_response.status_code
            result_msgs.append("There was a problem with finding your profile: got status code %s" % username_response.status_code)
            result_status = "error username"
    else:
         # Record the authentication error message
        result_msgs.append("There was a problem with authentication: got status code %s" % auth_response.status_code)
        result_status = "error auth"
        try:
            # create the new repo and push the app files to it
            result_status, result_msgs, created_repo_link, result_status = create_repo(auth_token, username, result_msgs)
        except:
            result_status = "error"
            result_msgs.append("Failed to create repo in user %s's public repos" % username)
    
    # render the results page with the status, and link to user's authorization for this app
    return render(request, "results.html", {'client_id': settings.CLIENT_ID,
                                            'result_status': result_status,
                                            'results_msgs': result_msgs,
                                            'created_repo_link': created_repo_link,
                                            'code': result_msgs})

def replicate_file(file_to_copy, username):
    
    # encode file to be pushed to repo
    file_to_copy = base64.b64encode(bytes(file_to_copy, 'utf-8'))
    # set up content to 
    contents_file = {'path': filepath,
                     'message':'replicated file',
                     'content': file_to_copy.decode("utf-8"),}
    requests.put('https://api.github.com/repos/%s/selfreplicatingapp/contents/%s' % (username, json.dumps(contents_file)))
    #response = requests.put('https://httpbin.org/put', data={'username': username, })

def create_repo(auth_token, username, result_msgs):
    created_repo_link = ''
    # create new repo in user's GitHub account
    #response = requests.post('https://api.github.com/user/repos', data=data, auth=(username, access_token))
    response = requests.post('https://api.github.com/%s/repos' % username, data={'name': 'selfreplicatingapp',
                                                                                 'description': 'This is an app that creates a copy of itself as a repo on github.',
                                                                                 'homepage': 'selfreplicator.herokuapp.com',
                                                                                 'auto_init': False})
    
    if response.status_code == 201:
        result_status = "success"
        result_msgs.append("successfully created new repo")
    else:
        # record repo creation error message
        result_status = "error creating repo"
        result_msgs.append("Failed to create new repo in user %s's GitHub account" % username)
            
    return result_status, result_msgs, created_repo_link, response.status_code
