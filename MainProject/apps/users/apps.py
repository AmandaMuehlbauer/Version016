# users/apps.py
from django.apps import AppConfig


#class UsersConfig(AppConfig):
 #   default_auto_field = "django.db.models.BigAutoField"
  #  name = "users"



class UsersConfig(AppConfig):
    name = 'apps.users'

    # add this function
    def ready(self):
        from . import signals

# users/__init__.py 
default_app_config = 'users.apps.UsersConfig'