set client_id=PASTE-CLIENT-ID-HERE
set client_secret=PASTE-CLIENT-SECRET-ID-HERE

ECHO Working from %CD% to set up project

python utils/setup_files.py %client_id% %client_secret% 

ECHO Set up for Django's settings.py file is complete 

python -m venv venv 

ECHO Created python virtual environment 

ECHO Press any key to continue to installing python libraries 
PAUSE 

venv\Scripts\activate.bat 

pip install -r requirements.txt 

ECHO Installed necessary python libs 
ECHO Finished setting up project 

PAUSE 