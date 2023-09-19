#URLsub/forms.py
from django import forms
from .models import  URLsub

class URLSubForm(forms.ModelForm):
    class Meta:
        model = URLsub
        #Exclude username from teh form
        exclude = ('username',)
        fields =('username', 'description', 'tags', 'url')

    # Define custom labels
    labels = {
        'description': 'Blog Description',
        'tags': 'Subject Tags',
        'url': 'Blog URL',
    }