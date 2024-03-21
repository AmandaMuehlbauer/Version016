#URLsub/forms.py
from django import forms
from .models import  URLsub, Description
from taggit.forms import TagField

class URLSubForm(forms.ModelForm):
    tags = TagField()
    class Meta:
        model = URLsub
        fields = ('url', 'title','description', 'tags')  # Include all relevant fields

    # Define custom labels
    labels = {
        'description': 'Blog Description',
        'title': 'Blog Title',
        'tags': 'Subject Tags',
        'url': 'Blog URL',
    }

class AdditionalDescriptionForm(forms.ModelForm):
    tags = TagField()

    class Meta:
        model = Description
        fields = ('description', 'tags')  # Exclude 'url' field

    # Define custom labels
    labels = {
        'description': 'Blog Description',
        'tags': 'Subject Tags',
    }