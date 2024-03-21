#URLsub/urls.py
from django.urls import path
from . import views
from .views import URLsubDetailView, add_additional_description

app_name = 'URLsub'  # Add the app namespace


urlpatterns = [
    path('urlsub/', views.urlsub, name='urlsub'),
    path('urlsub/thanks_url', views.url_thanks, name='thanks_url'),
    path('urlsub/<int:pk>/<slug:slug>/', URLsubDetailView.as_view(), name='urlsub_detail'),
    path('urlsub/<int:pk>/<slug:slug>/add_additional_description/', add_additional_description, name='add_additional_description'),

]