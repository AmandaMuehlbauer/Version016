#apps/URLsub/views.py
from django.shortcuts import render
from django.http import  HttpResponseRedirect
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
            description = form.cleaned_data['description']
            tags = form.cleaned_data['tags']  # Retrieve tags from the form

            # Check if a URLsub entry with the same URL already exists
            submission, created = URLsub.objects.get_or_create(
                user=user,
                url=url,
                defaults={
                    'description': description,
                }
            )

            if not created:
                # The URL submission already exists, increment the recommendations count
                submission.recommendations_count += 1
            else:
                # Set the description if a new submission is created
                submission.description = description

            # Handle tags for the submission
            submission.tags.set(tags)

            submission.save()

            return HttpResponseRedirect('thanks_url')
    else:
        form = URLSubForm()

    return render(request, 'URLsub/urlsub.html', {'form': form})

@login_required
def url_thanks(request):
    return render(request, 'URLsub/thanks_url.html', {})