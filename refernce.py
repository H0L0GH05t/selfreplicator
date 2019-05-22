from flask import render_template
from flask import request
from flask import jsonify

from app import app

import requests
import json
import sys
import os
import base64

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

def create_file(path, user, password, repo):
	with open(path) as f:
		filename = f.read()
	filename = base64.b64encode(bytes(filename, 'utf-8'))
	file = {'path': path, 'message':'add {}'.format(path), 'content': filename.decode("utf-8")}
	add_file = requests.put('https://api.github.com/repos/{}/{}/contents/{}'.format(user, repo, path), auth=(user, password), data=json.dumps(file))

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Dima'}
	return render_template('index.html', user=user)

@app.route('/replicate', methods=['POST'])
def replicate():
	user = request.form['name']
	password = request.form['password']
	repo = request.form['repo']

	payload = {'name': repo, 'description': 'this is a self-replication app.', 'auto_init': False}
	login = requests.post('https://api.github.com/user/repos', auth=(user, password), data=json.dumps(payload))

	for file in FILES:
		create_file(file, user, password, repo)

	if login.status_code == 201:
		return jsonify({'success' : 'Repo is replicated', 'user' : user})
	return jsonify({'error' : login.json()['message']})

@app.route('/delete', methods=['POST'])
def delete():
	user = request.form['name']
	password = request.form['password']
	repo = request.form['repo']
	deletion = requests.delete('https://api.github.com/repos/{}/{}'.format(user, repo), auth=(user, password))
	if deletion.status_code == 204:
		return jsonify({'success' : 'Repo is deleted'})
	return jsonify({'error' : deletion.json()['message']})