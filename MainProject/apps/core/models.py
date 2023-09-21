# Create your models here.
# core/models.py
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from apps.users.models import User

class Tag(models.Model):
    # Remove the 'name' field, as django-taggit handles tags internally
    tags = TaggableManager()

    class Meta:
        app_label = 'core'

    def __str__(self):
        return ', '.join(self.tags.names())  # Return a comma-separated list of tag names




class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='', blank=True, null=True)
    tags = TaggableManager()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('core:post', args=[str(self.id), self.slug])
    

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
    

#This model stores full blog recommendations
##This will come from data that has been scraped but for now it will be from 
class BlogFullRecommend(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    url = models.URLField(db_index=True)
    author = models.CharField(max_length=200, db_index=True, blank=True)
    content = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='', blank=True, null=True)
    tags = TaggableManager()
    last_updated = models.DateTimeField(blank=True)

    class Meta:
        ordering = ['-last_updated']

    def __str__(self):
        return self.title
    

#This model stores blog posts that have been scraped
#class BlogPostScraped(model.Model):
 #   parent_title = models.CharField(max_length=200, db_index=True)
  #  title=models.CharField(max_length=200, db_index=True)
   # url = models.URLField(db_index=True)
    #author = models.ForeignKey(max_length=200, db_index=True)
    #content = models.TextField(max_length=500, blank=True)
    #image = models.ImageField(upload_to='', blank=True, null=True)
    #tags = models.ManyToManyField(Tag, blank=True)
    #created_on = models.DateTimeField(blank=True)
    #updated_on = models.DateTimeField()

    #class Meta:
     #   ordering = ['-created_on']

   # def __str__(self):
    #    return self.title


#User interaction tracking
class UserPostInteraction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=255) 
    timestamp = models.DateTimeField(auto_now_add=True)