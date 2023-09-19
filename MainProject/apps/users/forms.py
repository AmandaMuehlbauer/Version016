# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Profile
import pytz


class SignUpForm(UserCreationForm):
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_password2(self):
        # Check if the two password fields match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


#class EditProfileForm(forms.Form):
 #   username = forms.CharField()
  #  about_me = forms.CharField(widget=forms.Textarea())
   # image = forms.ImageField(required=False)

   # def __init__(self, original_username, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
     #   self.original_username = original_username

    #def clean_username(self):
    #    """
     #   This function throws an exception if the username has already been 
      #  taken by another user
       # """

      #  username = self.cleaned_data['username']
       # if username != self.original_username:
        #    if User.objects.filter(username=username).exists():
         #       raise forms.ValidationError(
          #          'A user with that username already exists.')
        #return username
    

#class ProfileForm(forms.ModelForm):
 #   class Meta:
  #      model = Profile
   #     fields = ['interests',  'avatar', 'about_me', 'image']




class EditProfileForm(forms.ModelForm):
    about_me = forms.CharField(widget=forms.Textarea())
    banner = forms.ImageField(required=False)
    interests = forms.CharField(widget=forms.Textarea())
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['interests', 'avatar', 'about_me', 'banner']


