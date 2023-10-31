#URLsub/forms.py
from django import forms
from .models import  URLsub
from taggit.forms import TagField

class URLSubForm(forms.ModelForm):
    tags = TagField()
    class Meta:
        model = URLsub
        #Exclude username from the form
        exclude = ('username',)
        fields =('username', 'description', 'tags', 'url')

    # Define custom labels
    labels = {
        'description': 'Blog Description',
        'tags': 'Subject Tags',
        'url': 'Blog URL',
    }