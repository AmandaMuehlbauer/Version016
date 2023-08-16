#URLsub/views.py
from django.shortcuts import render
from django.http import  HttpResponseRedirect
from .forms import URLSubForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def urlsub(request):
    if request.method == 'POST':
      # create an instance of our form, and fill it with the POST data
        form = URLSubForm(request.POST)
        if form.is_valid():
          form.save()
        return HttpResponseRedirect('thanks_url')
    else:
  # this must be a GET request, so create an empty form
        form = URLSubForm()

    return render(request,
         'URLsub/urlsub.html',
         {'form': form})
@login_required()
def url_thanks(request):
    return render(request, 'URLsub/thanks_url.html', {})
