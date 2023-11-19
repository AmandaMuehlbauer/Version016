from django.urls import path
from . import views

urlpatterns = [
    path('posts/tag/<slug:tag_slug>/', views.post_list_by_tag, name='post_list_by_tag'),
    path('blogs/tag/<slug:tag_slug>/', views.blogs_list_by_tag, name='blogs_list_by_tag'),
]
