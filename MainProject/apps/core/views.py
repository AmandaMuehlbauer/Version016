# core/views.py
from django.shortcuts import render
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, 

)
from django.shortcuts import  redirect, render
from .models import Post, Comment
#from scraping.models import News
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from ..URLsub.models import URLsub
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.core import serializers 



from random import sample

class HomeView(ListView):
    template_name = 'core/home.html'
    context_object_name = 'blogs'
    paginate_by = 3  # Set the number of items per page


    def get_queryset(self):
        return URLsub.objects.all().order_by('-timestamp')  # Assuming 'timestamp' is the field representing the timestamp

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = context['blogs']

        # Fetch and assign tags to each blog
        for blog in blogs:
            blog.tags_list = blog.tags.all()

        context['blogs'] = blogs
        return context


class ForumView(ListView):
    template_name = 'core/forum.html'
    queryset = Post.objects.all()
    paginate_by = 10


    

class PostView(DetailView):
    model = Post
    template_name = 'core/forum_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.all()
        context['form'] = CommentForm()
        context['author_username'] = self.object.author.username
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            content = form.cleaned_data['content']
            author = request.user

            try:
                comment = Comment.objects.create(
                    author=author,
                    email=author.email,
                    content=content,
                    post=post
                )
                print("Comment created:", comment)  # Debugging line
            except Exception as e:
                print("Error creating comment:", str(e))  # Debugging line

        else:
            print("Form is not valid or user is not authenticated")  # Debugging line
            print("Form errors:", form.errors)  # Debugging line

        return redirect('core:post', pk=post.pk, slug=post.slug)
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "image", "tags"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['title'])
        obj.save()
        messages.success(self.request, 'Your post has been created successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        # After successfully creating the post, redirect to its detail view
        return reverse_lazy("core:post", kwargs={"pk": self.object.pk, "slug": self.object.slug})

    def get_form(self, form_class=None):
        # Initialize the form with an empty "tags" field for GET requests
        form = super().get_form(form_class=form_class)
        if self.request.method == 'GET':
            form.fields['tags'].initial = ''
        return form


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content", "image", "tags"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update

        return context

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been updated successfully.')
        return reverse_lazy("core:forum")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been deleted successfully.')
        return reverse_lazy("core:forum")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


#def SubmitURLView(request):

 #   context ={}
  #  form = SubmitURL()
   # context['form']= form
    #if request.POST:
     #   temp = request.POST['urlsubmission']
      #  print(temp)
    #return render(request, "core/submit_url.html", {"form":form})

def AboutView(request):
    return render(request, 'core/about.html', {})

def TrendingView(request):
    return render(request, 'core/trending.html')

def RecommendationsView(request):
    return render(request, 'core/recommendations.html')

def SubscriptionsView(request):
    return render(request, 'core/subscriptions.html')

def YourPostsView(request):
    return render(request, 'core/yourposts.html')

def SavedForLaterView(request):
    return render(request, 'core/savedforlater.html')

def LikedView(request):
    return render(request, 'core/liked.html')
#class RSSPageView(ListView):
 #   model = News
  #  template_name = 'core/rsstest.html'
   # context_object_name = 'articles' 
    #thing = News.objects.all()
    # assign "News" object list to the object "articles"
    # pass news objects as queryset for listview
    #print("Check thing:", thing)
  
    #def get_queryset(self):
     #   return News.objects.all()


