#apps/Search/views.py
from django.shortcuts import render
from django.db.models import Q
from .forms import SearchForm
from apps.core.models import Post, BlogFullRecommend  # Replace with your model
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from .documents import PostDocument
from elasticsearch.exceptions import NotFoundError
from django.urls import reverse



#import pdb; pdb.set_trace()

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




#def elastic_search_view(request):
  #  form = SearchForm(request.GET)
   # results = []
   # objects=[] #This stores the retrieved objects from model
   # post=[]


    #if form.is_valid():
     #   query = form.cleaned_data['query']
     #   print(query)
      #  client = Elasticsearch()  # Connect to the default Elasticsearch instance
     #   print(client)
       # s = Search(using=client, index='post')  # Replace 'myindex' with your index name
     #   print(s)
        #s = s.query("match", title=query)
     #   print(s)

        #response = s.execute()
       
       # print(response)
        #results = response.hits
    #    print(results)

    ##Want to use primary key to do query lookup
   
   #     try:
            # Execute the Elasticsearch query
    #        response = s.execute()

            # Extract primary keys (id) from Elasticsearch results
     #       pk_values = [hit.meta.id for hit in response]
           # print(pk_values)

            # Generate URLs for each retrieved Post object
      #      for post in objects:
       #         post.url = reverse('core:post', args=[str(post.id), post.slug])
                


        #        print(objects)

            #Generate the url 
         #   post = Post.objects.get(pk_values)
          #  print(post)

    #    except NotFoundError:
            # Handle the case when no results are found in Elasticsearch
     #       pass





  #  context = {
   #     'form': form,
    #    'results': results,
     #   'objects': objects
    #}
    #return render(request, 'search/elastic_search_results.html', context)



def elastic_search_view(request):
    form = SearchForm(request.GET)
    results = []
    objects = []  # This stores the retrieved objects from the model

    if form.is_valid():
        query = form.cleaned_data['query']
        client = Elasticsearch()  # Connect to the default Elasticsearch instance
        s = Search(using=client, index='post')  # Replace 'myindex' with your index name
        s = s.query("match", title=query)

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
