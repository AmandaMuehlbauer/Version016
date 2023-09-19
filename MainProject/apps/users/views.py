# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm, EditProfileForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from django.contrib import messages
from django.utils import timezone




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def log_in(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]  # Change to 'username'
            password = form.cleaned_data["password"]
            # We check if the data is correct
            user = authenticate(username=username, password=password)  # Change to 'username'
            if user:  # If the returned object is not None
                login(request, user)  # we connect the user
                return redirect('core:home')
            else:  # otherwise an error will be displayed
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect(reverse('users:login'))


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'users/profile.html', {'profile': profile, 'user': user})



@login_required
def edit_profile(request, username):
    user = request.user
  #  print(user)
    profile = user.profile


    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
           
            profile_url = reverse('users:profile', args=[username])  # Use the 'profile' URL name here

            
            # Redirect to the user's profile page after editing
            return redirect(profile_url)
    else:
        form = EditProfileForm(instance=profile)

         # Exclude the 'username' field from the form
    form.fields.pop('username', None)

    context = {
        'form': form,
    }

    return render(request, 'users/edit_profile.html', context)


