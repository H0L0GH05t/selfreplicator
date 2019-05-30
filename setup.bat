@echo off 

ECHO Working from %CD% to set up project. Running could take several minutes.

python -m venv venv 

ECHO Created python virtual environment, installing libraries... 

pip install -r requirements.txt 

ECHO Installed necessary python libs

python utils/setup_files.py 

ECHO Set up for Django's settings.py file is complete. Creating venv... 

ECHO Finished setting up project 

PAUSE 