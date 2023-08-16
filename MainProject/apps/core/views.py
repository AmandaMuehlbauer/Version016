# core/views.py
from django.shortcuts import render
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, 
    View
)
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Comment
from scraping.models import News
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .forms import CommentForm, SubmitURL
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.views import generic
from django.core.mail import send_mail

class HomeView(ListView):
    template_name = 'core/home.html'
    queryset = Post.objects.all()
    paginate_by = 10

class PostView(DetailView):
    model = Post
    template_name = 'core/post.html'
    thing1 = Post.objects.all()
   # print("thing1", thing1)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        slug = self.kwargs["slug"]

        form = CommentForm()
        post = get_object_or_404(Post, pk=pk, slug=slug)
        comments = post.comment_set.all()

        stuff=get_object_or_404(Post, id=self.kwargs['pk'])

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            comments = Comment.objects.create(
                name=name, email=email, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "image", "tags"]

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been created successfully.')
        return reverse_lazy("core:home")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['title'])
        obj.save()
        return super().form_valid(form)

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
        return reverse_lazy("core:home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been deleted successfully.')
        return reverse_lazy("core:home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


def SubmitURLView(request):

    context ={}
    form = SubmitURL()
    context['form']= form
    if request.POST:
        temp = request.POST['urlsubmission']
        print(temp)
    return render(request, "core/submit_url.html", {"form":form})

def AboutView(request):
    return render(request, 'core/about.html', {})



class RSSPageView(ListView):
    model = News
    template_name = 'core/rsstest.html'
    context_object_name = 'articles' 
    thing = News.objects.all()
    # assign "News" object list to the object "articles"
    # pass news objects as queryset for listview
    print("Check thing:", thing)
  
    def get_queryset(self):
        return News.objects.all()


