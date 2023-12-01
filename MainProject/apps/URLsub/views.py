#apps/URLsub/views.py
from django.shortcuts import render
from django.http import  HttpResponseRedirect, HttpResponseNotFound
from .forms import URLSubForm
from django.contrib.auth.decorators import login_required
from .models import URLsub
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404






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


##View to see individual blogs and their descriptions, reviews authors etc
class URLsubDetailView(DetailView):
    model = URLsub
    template_name = 'URLsub/urlsub_detail.html'  # Create a template for the detail view
    context_object_name = 'urlsub'

    def get_object(self, queryset=None):
        # Retrieve the object based on both primary key and slug
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        return get_object_or_404(URLsub, pk=pk, slug=slug)