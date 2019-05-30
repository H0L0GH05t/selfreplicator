@echo off 

ECHO Working from %CD% to set up project. 
ECHO This will take a few minutes. 
ECHO Creating venv... 

python -m venv venv 

ECHO Installing python libraries... 

pip install -r requirements.txt 

ECHO Setting up Django for this project... 

python utils/setup_files.py 

ECHO Finished setup 

PAUSE 