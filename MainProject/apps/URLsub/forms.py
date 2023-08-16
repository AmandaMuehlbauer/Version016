#URLsub/forms.py
from django import forms
from .models import  URLsub

class URLSubForm(forms.ModelForm):
    class Meta:
        model = URLsub
        fields =('username', 'description', 'tags', 'url')