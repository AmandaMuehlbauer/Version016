from django.db import models
from django.contrib import admin



# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=100)
    content = models.TextField()

