from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from django.utils.text import slugify

class URLsub(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.TextField()
    description = models.TextField()
    tags = TaggableManager()  # Specify the through parameter
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=200, default='default-slug-value')  # Add the SlugField

    class Meta:
        unique_together = ('url', 'user')  # Add this unique constraint

    def author_username(self):
        return self.user.username  # Access the username of the user

    def author_email(self):
        return self.user.email 
    
    def save(self, *args, **kwargs):
        # Generate a slug before saving
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
