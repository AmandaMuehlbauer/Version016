#URLsub/urls.py
from django.urls import path
from . import views
from .views import URLsubDetailView

app_name = 'URLsub'  # Add the app namespace


urlpatterns = [
    path('urlsub/', views.urlsub, name='urlsub'),
    path('urlsub/thanks_url', views.url_thanks, name='thanks_url'),
    path('urlsub/<int:pk>/<slug:slug>/', URLsubDetailView.as_view(), name='urlsub_detail'),

]