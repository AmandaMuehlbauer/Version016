#apps/Search/views.py
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import SearchForm
from apps.core.models import Post, BlogFullRecommend  # Replace with your model
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from .documents import PostDocument
from elasticsearch.exceptions import NotFoundError
from django.urls import reverse
from .models import SearchHistory
import os



#this is a basic search/lookup with the database. Not used in Jidder

def search_view(request):
    form = SearchForm()
    results = []


    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(title__icontains=query)
        
        context = {
            'form': form,
            'results': results
        }

    return render(request, 'search/search_results.html', context)


#This is the function that is used in the Jidder searchbar. It uses elasticsearch. 

def elastic_search_view(request):
    form = SearchForm(request.GET)
    results = []
    objects = []  # This stores the retrieved objects from the model

    if form.is_valid():
        query = form.cleaned_data['query']
        #client = Elasticsearch()  # Connect to the default Elasticsearch instance
        #client = Elasticsearch(hosts=[{'host': 'jidder-elasticsearch', 'port': 9200}])
        if os.environ.get("ENVIRONMENT") == "production":
    # Use production Elasticsearch settings
            client = Elasticsearch(hosts=[{'host': 'jidder-elasticsearch', 'port': 9200}])
        else:
    # Use development Elasticsearch settings
            client = Elasticsearch()

        s = Search(using=client, index='post')  # Replace 'myindex' with your index name
        s = s.query("match", title=query)
        print("Form is valid")

        res = PostDocument.search().query("match", title="cat")

        print(res)

        # Save the search history to the database
        if request.user.is_authenticated:
            search_history = SearchHistory(user=request.user, query=query)
            search_history.save()

        response = s.execute()
        results = response.hits

        # Extract primary keys (id) from Elasticsearch results
        pk_values = [hit.meta.id for hit in response]

        # Look up full Post objects using the primary keys
        if pk_values:
            objects = Post.objects.filter(id__in=pk_values)

            # Generate URLs for each retrieved Post object
            for post in objects:
                post.url = reverse('core:post', args=[str(post.id), post.slug])
                print(post.url)

    context = {
        'form': form,
        'results': results,
        'objects': objects
    }
    return render(request, 'search/elastic_search_results.html', context)


#Function to display search results back to users:

def view_search_history(request):
    if request.user.is_authenticated:
        search_history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
        return render(request, 'Search/search_history.html', {'search_history': search_history})
    else:
        # Handle the case when the user is not authenticated
        return redirect('users:login')  # Redirect to the login page or handle as needed

