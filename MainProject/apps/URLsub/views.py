#apps/URLsub/views.py
from django.shortcuts import render
from django.http import  HttpResponseRedirect, HttpResponseNotFound
from .forms import URLSubForm
from django.contrib.auth.decorators import login_required
from .models import URLsub, Description, Tag
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
            tags = form.cleaned_data['tags']

            existing_submission = URLsub.objects.filter(url=url).first()

            if existing_submission:
                existing_submission.title = title
                existing_submission.tags.set(tags)
                existing_submission.save()
                submission = existing_submission
            else:
                submission = URLsub.objects.create(
                    user=user,
                    url=url,
                    title=title,
                )
                submission.tags.set(tags)

            description_text = form.cleaned_data['description']
            description = Description.objects.create(urlsub=submission, description=description_text, user=user)
            description_tags = description.tags.all()

            description.tags.set(tags)

            return HttpResponseRedirect('thanks_url')

    else:
        form = URLSubForm()

    all_tags = Tag.objects.values_list('name', flat=True).distinct()

    return render(request, 'URLsub/urlsub.html', {'form': form, 'all_tags': all_tags, 'description_tags': description_tags})

@login_required
def url_thanks(request):
    return render(request, 'URLsub/thanks_url.html', {})


##View to see individual blogs and their descriptions, reviews authors etc
class URLsubDetailView(DetailView):
    model = URLsub
    template_name = 'URLsub/urlsub_detail.html'  # Create a template for the detail view
    context_object_name = 'urlsub'
    paginate_by = 10 #set number of items per page

    def get_object(self, queryset=None):
        # Retrieve the object based on both primary key and slug
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        return get_object_or_404(URLsub, pk=pk, slug=slug)