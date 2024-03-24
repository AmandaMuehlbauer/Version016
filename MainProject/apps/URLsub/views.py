#apps/URLsub/views.py
from django.shortcuts import render, redirect
from django.http import  HttpResponseRedirect, HttpResponseNotFound
from .forms import URLSubForm, AdditionalDescriptionForm
from django.contrib.auth.decorators import login_required
from .models import URLsub, Description, Tag
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



@login_required
def urlsub(request):
    description_tags = None  # Define description_tags outside of the conditional blocks

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
            description_tags = description.tags.all()  # Update description_tags here

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
    template_name = 'URLsub/urlsub_detail.html'
    context_object_name = 'urlsub'
    paginate_by = 10

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        return get_object_or_404(URLsub, pk=pk, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_descriptions = self.object.additional_descriptions.order_by('timestamp')
        paginator = Paginator(additional_descriptions, self.paginate_by)
        page_number = self.request.GET.get('page')
        additional_descriptions_page = paginator.get_page(page_number)
        context['additional_descriptions_page'] = additional_descriptions_page
        return context


@login_required
def add_additional_description(request, pk, slug):
    urlsub = get_object_or_404(URLsub, pk=pk, slug=slug)
    
    if request.method == 'POST':
        form = AdditionalDescriptionForm(request.POST)
        if form.is_valid():
            additional_description = form.save(commit=False)
            additional_description.urlsub = urlsub
            additional_description.user = request.user
            additional_description.save()

            form.save_m2m()  # Save the tags associated with the additional description

            return redirect('URLsub:urlsub_detail', pk=pk, slug=slug)  # Redirect to the URLsub detail page with slug
    else:
        form = AdditionalDescriptionForm()
    
    return render(request, 'URLsub/add_additional_description.html', {'form': form, 'urlsub': urlsub})