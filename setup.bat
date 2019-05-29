@echo off 

ECHO Working from %CD% to set up project 

python utils/setup_files.py 

ECHO Set up for Django's settings.py file is complete. Creating venv... 

python -m venv venv 

ECHO Created python virtual environment, installing libraries... 

pip install -r requirements.txt 

ECHO Installed necessary python libs 

ECHO Finished setting up project 

PAUSE 