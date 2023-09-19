from django.urls import path
from . import views

app_name = 'Search'

urlpatterns = [
    # Other URL patterns
    path('search/', views.search_view, name='search_view'),
    path('elastic-search/', views.elastic_search_view, name='elastic_search_view'),

]
