#apps/URLsub/models.py
from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings


class URLsub(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField()
    description = models.TextField()
    tags = TaggableManager()
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('url', 'user')  # Add this unique constraint



def author_username(self):
    return self.user.username  # Access the username of the user

def author_email(self):
    return self.user.email 
