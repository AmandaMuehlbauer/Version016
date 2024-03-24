# core/views.py
from django.shortcuts import render
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, 

)
from django.shortcuts import  redirect, render, get_object_or_404
from .models import Post, Comment
#from scraping.models import News
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .forms import CommentForm, URLSpecificPostForm
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
    paginate_by = 12  # Set the number of items per page


    def get_queryset(self):
        return URLsub.objects.all().order_by('-timestamp')  # Set 'timestamp' as the field to sort by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = context['blogs']

        # Fetch and assign tags to each blog
        for blog in blogs:
            blog.tags_list = blog.tags.all()

        # Add slug and pk for each URLsub object
        for blog in blogs:
            blog.slug = blog.slug  # Assuming URLsub model has a 'slug' field
            blog.pk = blog.pk  # Assuming URLsub model has a 'pk' field

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


#Create a view for Posts associated with a specific URL

class URLSpecificPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = URLSpecificPostForm
    template_name = 'core/url_specific_post_create.html'

    def form_valid(self, form):
        # Associate the URLsub instance with the Post object
        urlsub_pk = self.kwargs.get('pk')
        urlsub_slug = self.kwargs.get('slug')
        urlsub = get_object_or_404(URLsub, pk=urlsub_pk, slug=urlsub_slug)
        
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['title'])
        obj.urlsub = urlsub  # Set the URLsub instance
        obj.save()
        messages.success(self.request, 'Your post has been created successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("core:url_specific_post", kwargs={"pk": self.object.urlsub.pk, "slug": self.object.urlsub.slug, "post_pk": self.object.pk, "post_slug": self.object.slug})
    
    def get_initial(self):
        initial = super().get_initial()
        # Retrieve the URLSub instance from the URL parameters
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        urlsub = get_object_or_404(URLsub, pk=pk, slug=slug)
        initial['urlsub'] = urlsub
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the URLsub title to the context
        context['urlsub_title'] = self.get_initial()['urlsub'].title
        return context

    def get_form(self, form_class=None):
        # Initialize the form with an empty "tags" field for GET requests
        form = super().get_form(form_class=form_class)
        if self.request.method == 'GET':
            form.fields['tags'].initial = ''
        return form
    

class URLSpecificPostView(DetailView):
    model = Post  
    template_name = 'core/url_specific_post.html'
    context_object_name = 'url_specific_post'

    def get_object(self, queryset=None):
        urlsub_pk = self.kwargs.get('pk')
        urlsub_slug = self.kwargs.get('slug')
        post_pk = self.kwargs.get('post_pk')
        post_slug = self.kwargs.get('post_slug')

        urlsub = get_object_or_404(URLsub, pk=urlsub_pk, slug=urlsub_slug)
        post = get_object_or_404(Post, pk=post_pk, slug=post_slug, urlsub=urlsub)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urlsub'] = self.object.urlsub
        context['comments'] = self.object.comment_set.all()
        context['form'] = CommentForm()
        context['author_username'] = self.object.author.username
        return context
    
    def get_absolute_url(self):
        return reverse('core:url_specific_post', kwargs={'pk': self.urlsub.pk, 'slug': self.urlsub.slug, 'post_pk': self.pk, 'post_slug': self.slug})


    def post(self, request, *args, **kwargs):
        url_specific_post = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            content = form.cleaned_data['content']
            author = request.user

            try:
                comment = Comment.objects.create(
                    author=author,
                    email=author.email,
                    content=content,
                    post=url_specific_post
                )
                print("Comment created:", comment)  # Debugging line
            except Exception as e:
                print("Error creating comment:", str(e))  # Debugging line

        else:
            print("Form is not valid or user is not authenticated")  # Debugging line
            print("Form errors:", form.errors)  # Debugging line


        # Redirect to the URL specific post's URL
        return redirect('core:url_specific_post', pk=url_specific_post.urlsub.pk, slug=url_specific_post.urlsub.slug, post_pk=url_specific_post.pk, post_slug=url_specific_post.slug)


class URLSpecificForumView(ListView):
    template_name = 'core/discussion.html'
    queryset = Post.objects.all()
    paginate_by = 12

    def get_queryset(self):
        # Get the URLsub id and slug from the URL parameters
        urlsub_id = self.kwargs.get('pk')
        urlsub_slug = self.kwargs.get('slug')
        
        # Filter posts by the URLsub id and slug
        queryset = Post.objects.filter(urlsub_id=urlsub_id, urlsub__slug=urlsub_slug)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
    # Get the URLsub object
        urlsub = get_object_or_404(URLsub, pk=self.kwargs.get('pk'))
    
    # Add URLsub title, URL, pk, and slug to the context
        context['urlsub_title'] = urlsub.title
        context['urlsub_url'] = urlsub.url
        context['urlsub_pk'] = urlsub.pk
        context['urlsub_slug'] = urlsub.slug
    
        return context