#apps/URLsub/views.py
from django.shortcuts import render
from django.http import  HttpResponseRedirect, HttpResponseNotFound
from .forms import URLSubForm
from django.contrib.auth.decorators import login_required
from .models import URLsub


@login_required
def urlsub(request):  

    if request.method == 'POST':
        form = URLSubForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            user = request.user
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            tags = form.cleaned_data['tags']

            # Check if the URL submission already exists for the user
            submission = URLsub.objects.filter(user=user, url=url).first()

            if submission:
                # If the submission exists, update its fields
                submission.title = title
                submission.description = description
                submission.tags.set(tags)
                submission.save()
            else:
                # Create a new URL submission
                submission = URLsub.objects.create(
                    user=user,
                    url=url,
                    title=title,
                    description=description
                )
                submission.tags.set(tags)

            return HttpResponseRedirect('thanks_url')
    else:
        form = URLSubForm()

    return render(request, 'URLsub/urlsub.html', {'form': form})

@login_required
def url_thanks(request):
    return render(request, 'URLsub/thanks_url.html', {})

