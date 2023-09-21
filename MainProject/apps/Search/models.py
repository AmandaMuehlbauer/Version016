#apps/Search/models.py

from django.db import models
from django.conf import settings  # If you want to associate search history with users

class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Add more fields as needed to store additional information about the search or results
