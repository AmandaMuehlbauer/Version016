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

def elastic_search_view_draft001(request):
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

        try:
            # Attempt to connect to Elasticsearch
            client.ping()
            print("Successfully connected to Elasticsearch server")
        except ConnectionError:
            # If the connection fails, handle the error as needed
            # For example, you can log the error or return an error response
            return HttpResponse("Failed to connect to Elasticsearch server")

        # The rest of your code for Elasticsearch query and processing goes here
        # ...


        s = Search(using=client, index='post').params(request_timeout=30)  # create a Search object
        s = s.query('multi_match', query=query, fields=['title', 'content']) #define the search query


        try:
            response = s.execute()
            print(response.success())
        except Exception as e:
            print(f"An error occurred when executing the Elasticsearch query: {e}")
        print("response:")
        print(response)
        results = response.hits
        print("results:")
        print(results)
        # Extract primary keys (id) from Elasticsearch results
        pk_values = [hit.meta.id for hit in response]
        print("pk_values")
        print(pk_values)
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

            # Save the search history to the database
    if request.user.is_authenticated:
        search_history = SearchHistory(user=request.user, query=query)
        search_history.save()

    return render(request, 'search/elastic_search_results.html', context)

def elastic_search_view(request):
    form = SearchForm(request.GET)
    results = []
    objects = []

    if form.is_valid():
        query = form.cleaned_data['query']

        # Determine the Elasticsearch server based on the environment
        if os.environ.get("ENVIRONMENT") == "production":
            es_server = 'jidder-elasticsearch:9200'  # Use the production server
        else:
            es_server = 'localhost:9200'  # Use the development server

        try:
            # Establish an Elasticsearch connection
            client = Elasticsearch(hosts=[es_server])

            # Ping the Elasticsearch server to check the connection
            if not client.ping():
                return HttpResponse("Failed to connect to Elasticsearch server")

            # Build and execute the Elasticsearch search
            response = client.search(
                index='post',  # Replace with your index name
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "content"]
                        }
                    }
                }
            )

            results = response['hits']['hits']

            if request.user.is_authenticated:
                # Save the search history to the database
                search_history = SearchHistory(user=request.user, query=query)
                search_history.save()

            objects = Post.objects.filter(id__in=[result['_id'] for result in results])

        except ConnectionError:
            return HttpResponse("Failed to connect to Elasticsearch server")
        except ElasticsearchException as e:
            print(f"An error occurred when executing the Elasticsearch query: {e}")

    context = {
        'form': form,
        'results': results,
        'objects': objects,
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


