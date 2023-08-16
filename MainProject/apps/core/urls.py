# core/urls.py
from django.urls import path
from . import views
from .views import HomeView, PostView, PostCreateView, PostUpdateView, PostDeleteView, RSSPageView
#, AddDislike, AddLike

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<pk>/<slug:slug>/', PostView.as_view(), name='post'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
  #  path('submit_url/', views.SubmitURLView, name='submit_url'),
    path('About/', views.AboutView, name='about'),
    path('rsstest/', RSSPageView.as_view(), name="rsstest"),
#    path('contact-us/', views.contact, name='contact'),
#    path('contact-us/success', views.contact_success, name='success')
]