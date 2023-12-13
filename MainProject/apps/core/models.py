# Create your models here.
# core/models.py
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from apps.users.models import User
from apps.URLsub.models import URLsub

#class Tag(models.Model):
    # Remove the 'name' field, as django-taggit handles tags internally
#    tags = TaggableManager()

 #   class Meta:
  #      app_label = 'core'

   # def __str__(self):
    #    return ', '.join(self.tags.names())  # Return a comma-separated list of tag names




class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='Post_image/', blank=True, null=True)
    tags = TaggableManager(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    urlsub = models.ForeignKey(URLsub, on_delete=models.CASCADE, related_name='related_posts', blank=True, null=True)


    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('core:post', args=[str(self.id), self.slug])
    
    def author_username(self):
        return self.author.username

    def author_email(self):
        return self.author.email
    

class Comment(models.Model):
    #name = models.CharField(max_length=50)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering = ('-created',)

    def __str__(self):
       return 'Comment by {}'.format(self.author.username)
    
    def author_username(self):
        return self.author.username

    def author_email(self):
        return self.author.email
    

#This model stores full blog recommendations
##This will come from data that has been scraped but for now it will be from 
class BlogFullRecommend(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    url = models.URLField(db_index=True)
    author = models.CharField(max_length=200, db_index=True, blank=True)
    content = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='BlogFullRecommend_image/', blank=True, null=True)
    tags = TaggableManager(blank=True)
    last_updated = models.DateTimeField(blank=True)

    class Meta:
        ordering = ['-last_updated']

    def __str__(self):
        return self.title
    

