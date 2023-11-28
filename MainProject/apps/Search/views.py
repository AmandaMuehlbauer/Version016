#apps/Search/views.py
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import SearchForm
from apps.core.models import Post, BlogFullRecommend   # Replace with your model
from apps.URLsub.models import URLsub
from elasticsearch import Elasticsearch
#from elasticsearch_dsl import Search
from .documents import PostDocument
from elasticsearch.exceptions import NotFoundError
from django.urls import reverse
from .models import SearchHistory
import os
import logging
from elasticsearch.exceptions import ConnectionError, ElasticsearchException
import re

# Define a list of common stop words
stop_words = ["the", "and", "is", "this", "a", "an", "of", "in", "to", "for"]

def remove_stop_words(query):
    # Split the query into individual words
    words = query.split()

    # Remove common stop words
    clean_words = [word for word in words if word.lower() not in stop_words]

    # Rejoin the remaining words into a clean query
    clean_query = " ".join(clean_words)

    return clean_query


def parse_post_query(query):
    words = query.split()
    operators = {"AND": Q.AND, "OR": Q.OR}
    q_objects = []

    post_fields = [field.name for field in Post._meta.get_fields()]

    for word in words:
        if word.upper() in operators:
            operator = operators[word.upper()]
            q_objects.append(operator)
        else:
            cleaned_word = remove_stop_words(word)
            post_query = None

            if all(field in post_fields for field in ['title', 'content', 'tags']):
                post_query = (
                    Q(title__icontains=cleaned_word) |
                    Q(content__icontains=cleaned_word) |
                    Q(tags__name__icontains=cleaned_word)
                )

            if post_query is not None:
                q_objects.append(post_query)

    boolean_query = q_objects[0] if q_objects else Q()
    for i in range(1, len(q_objects), 2):
        if i + 1 < len(q_objects):
            boolean_query = boolean_query & q_objects[i + 1]

    return boolean_query


def parse_urlsub_query(query):
    words = query.split()
    operators = {"AND": Q.AND, "OR": Q.OR}
    q_objects = []

    urlsub_fields = [field.name for field in URLsub._meta.get_fields()]

    for word in words:
        if word.upper() in operators:
            operator = operators[word.upper()]
            q_objects.append(operator)
        else:
            cleaned_word = remove_stop_words(word)
            urlsub_query = None

            if all(field in urlsub_fields for field in ['title', 'description', 'tags']):
                urlsub_query = (
                    Q(title__icontains=cleaned_word) |
                    Q(description__icontains=cleaned_word) |
                    Q(tags__name__icontains=cleaned_word)
                )

            if urlsub_query is not None:
                q_objects.append(urlsub_query)

    boolean_query = q_objects[0] if q_objects else Q()
    for i in range(1, len(q_objects), 2):
        if i + 1 < len(q_objects):
            boolean_query = boolean_query & q_objects[i + 1]

    return boolean_query

def search_view(request):
    form = SearchForm()
    results_post = []
    results_urlsub = []

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            boolean_query_post = parse_post_query(query)
            boolean_query_urlsub = parse_urlsub_query(query)

            results_post = Post.objects.filter(boolean_query_post).distinct()
            results_urlsub = URLsub.objects.filter(boolean_query_urlsub).distinct()

            if request.user.is_authenticated:
                search_history = SearchHistory(user=request.user, query=query)
                search_history.save()

    context = {
        'form': form,
        'results_post': results_post,
        'results_urlsub': results_urlsub,
    }

    return render(request, 'Search/search_results.html', context)

#This is the function that is used in the Jidder searchbar. It uses elasticsearch. 

def elastic_search_view_001(request):
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

    return render(request, 'Search/elastic_search_results.html', context)



def elastic_search_view(request):
    form = SearchForm(request.GET)
    results = []
    objects = []  # This stores the retrieved objects from the model

    if form.is_valid():
        query = form.cleaned_data['query']
        
        if os.environ.get("ENVIRONMENT") == "production":
            # Use production Elasticsearch settings
            client = Elasticsearch(hosts=['jidder-elasticsearch:9200'])
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

        try:
            response = client.search(
                index='post',
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "content"]
                        }
                    }
                }
            )
            print(response)
            results = response['hits']['hits']
        except Exception as e:
            print(f"An error occurred when executing the Elasticsearch query: {e}")

        # Extract primary keys (id) from Elasticsearch results
        pk_values = [hit['_id'] for hit in results]
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

    return render(request, 'Search/elastic_search_results.html', context)




#Function to display search results back to users:

def view_search_history(request):
    if request.user.is_authenticated:
        search_history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
        return render(request, 'Search/search_history.html', {'search_history': search_history})
    else:
        # Handle the case when the user is not authenticated
        return redirect('users:login')  # Redirect to the login page or handle as needed


