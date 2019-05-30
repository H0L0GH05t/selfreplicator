import sys, os, re
from django.utils.crypto import get_random_string

# This script edits the settings file with a new secret id

def generate_secret_key(length=50):
    # https://github.com/mrouhi13/djecrety
    """
        Return a 50 character random string usable as a SECRET_KEY setting value.
    """
    try:
        length = int(length)
    except ValueError:
        length = 50
    except TypeError:
        length = 50

    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

    return get_random_string(length, chars)

def create_settings():
    
    # read the file containing the ids we need for the settings file
    with open('SETUP.txt', 'r') as f:
        setup_file = f.read() 
    
    client_id = ""
    client_secret_id =""
    
    m = re.match(r"client_id=(?P<client_id>\w+)\s*client_secret_id=(?P<client_secret_id>\w+)\s*", setup_file)
    if m:
        client_id = m.group('client_id')
        client_secret_id = m.group('client_secret_id')
    
    new_secret_key = generate_secret_key()
    print("Generated new secret key for Django project")
    
    try:
        # read the template settings file
        with open('githubapps/settings-template.py', 'r') as f:
            settings_file = f.read()
        
        # replaces the place holder text with the provided client ids, and generated secret
        settings_file = settings_file.replace("SECRET_KEY = ''", "SECRET_KEY = '%s'" % new_secret_key)
        settings_file = settings_file.replace("CLIENT_ID = ''", "CLIENT_ID = '%s'" % client_id)
        settings_file = settings_file.replace("CLIENT_SECRET = ''", "CLIENT_SECRET = '%s'" % client_secret_id)
        
        # write the new settings file
        with open('githubapps/settings.py','w') as f:
            f.write(settings_file)
        print("Successfully created new Django settings file")
    except Exception as e:
        print("Error generating new settings file: %s" % e)
    
    # create the staticfiles folder
    if not os.path.exists('staticfiles'):
        os.makedirs('staticfiles')
        print("Created staticfiles folder for running locally")
    
if __name__ == "__main__":
    create_settings()
    print("Django project setup script finished")