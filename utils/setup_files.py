import sys
from django.utils.crypto import get_random_string

# This script edits the settings file with a new secret id

def create_settings(client_id, client_secret):
    
    new_secret_key = generate_secret_key()
    
    try:
        with open('githubapps/settings-template.py', 'r') as f:
            settings_file = f.read()
            
        settings_file = settings_file.replace("SECRET_KEY = ''", "SECRET_KEY = '%s'" % new_secret_key)
        settings_file = settings_file.replace("CLIENT_ID = ''", "CLIENT_ID = '%s'" % client_id)
        settings_file = settings_file.replace("CLIENT_SECRET = ''", "CLIENT_SECRET = '%s'" % client_secret)
        
        with open('githubapps/settings.py','w') as f:
            f.write(settings_file)
    except Exception as e:
        print("Error generating new settings file: %s" % e)
    print("Created new settings file")

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
    
if __name__ == "__main__":
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    create_settings(client_id, client_secret)
    print("Setup script finished")