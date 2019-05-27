@echo off
CLS

IF NOT (%1)==() GOTO %1

:MENU
IF NOT (%1)==() GOTO EOF
ECHO.

cd utils

python generate_secret_id.py

cd ..

python manage.py migrate