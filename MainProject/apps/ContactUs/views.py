#ContactUs/views.py
from django.shortcuts import render
from django.http import  HttpResponseRedirect
from .forms import ContactUsForm

# Create your views here.
def contact(request):
    if request.method == 'POST':
      # create an instance of our form, and fill it with the POST data
        form = ContactUsForm(request.POST)
        if form.is_valid():
          form.save()
        return HttpResponseRedirect('success')
    else:
  # this must be a GET request, so create an empty form
        form = ContactUsForm()

    return render(request,
         'ContactUs/contact.html',
         {'form': form})

def contact_success(request):
    return render(request, 'ContactUs/success.html', {})
