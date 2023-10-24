# core/urls.py
from django.urls import path
from . import views
from .views import HomeView, PostView, PostCreateView, PostUpdateView, PostDeleteView,  ForumView, YourPostsView, SavedForLaterView, LikedView
#, AddDislike, AddLike

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('Forum', ForumView.as_view(), name='forum'),
    path('post/<int:pk>/<slug:slug>/', PostView.as_view(), name='post'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),

    path('post/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('About/', views.AboutView, name='about'),
    path('Trending/', views.TrendingView, name='trending'),
    path('Recommendations/', views.RecommendationsView, name='recommendations'),
    path('Subscriptions/', views.SubscriptionsView, name='subscriptions'),

    path('YourPosts/', views.YourPostsView, name='yourposts'),

    path('SavedForLater/', views.SavedForLaterView, name='savedforlater'),
    path('Liked/', views.LikedView, name='liked'),
 #   path('rsstest/', RSSPageView.as_view(), name="rsstest"),

]