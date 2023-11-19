#URLsub/forms.py
from django import forms
from .models import  URLsub
from taggit.forms import TagField

class URLSubForm(forms.ModelForm):
    tags = TagField()
    class Meta:
        model = URLsub
        fields = ('url', 'description', 'tags')  # Include all relevant fields

    # Define custom labels
    labels = {
        'description': 'Blog Description',
        'tags': 'Subject Tags',
        'url': 'Blog URL',
    }