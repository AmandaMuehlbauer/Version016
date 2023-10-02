#blog/development_settings.py

# Import settings from the main settings.py file
#from .settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent
# Import settings from the main settings.py file


import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'blog'),
        'USER': os.environ.get('DB_USER', 'test'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'hey little songbird gimme a song'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
