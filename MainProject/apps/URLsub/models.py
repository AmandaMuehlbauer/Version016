#apps/URLsub/models.py
from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings

# Create your models here.



class URLsub(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    description = models.TextField()
    tags = TaggableManager()
    url = models.CharField(max_length=200, default="", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "URL Submissions" 

    def author_username(self):
        return self.username.username

    def author_email(self):
        return self.username.email