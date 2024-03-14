# core/forms.py
from django import forms
from .models import Comment, Post
from taggit.forms import TagField

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('email', 'content')  # Exclude 'author' field from the form
        exclude = ['author']  # Alternatively, you can use exclude as a list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['content'].required = True



class SubmitURL(forms.Form):
    url = forms.URLField(label='URL', max_length=200)


#class ContactUsForm(forms.ModelForm):
 #   class Meta:
  #      model = Contact
   #     fields =('name', 'email', 'content')


class PostForumForm(forms.ModelForm):
    tags = TagField()
    class Meta:
        model = Post
        fields = ["title", "content", "image", "tags"]



class URLSpecificPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image", "tags"]