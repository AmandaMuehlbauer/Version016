# core/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')

class SubmitURL(forms.Form):
    url = forms.URLField(label='URL', max_length=200)


#class ContactUsForm(forms.ModelForm):
 #   class Meta:
  #      model = Contact
   #     fields =('name', 'email', 'content')
    