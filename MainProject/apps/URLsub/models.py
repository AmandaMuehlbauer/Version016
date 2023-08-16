from django.db import models
#from taggit.managers import TaggableManager
from django.conf import settings

# Create your models here.



class URLsub(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    description = models.TextField()
    tags = models.CharField(max_length=200, default="", null=True, blank=True)
    url = models.URLField(max_length = 200)
    timestamp = models.DateTimeField(auto_now_add=True)