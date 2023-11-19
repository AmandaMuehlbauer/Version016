#apps/SubjectTags/views.py
from django.shortcuts import render
from taggit.models import Tag
from apps.core.models import Post  # Assuming 'Post' is the model from the 'core' app
from apps.URLsub.models import URLsub  # Assuming 'URLSub' is the model from the 'URLSub' app
 
def post_list_by_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    print(tag)
    posts = Post.objects.filter(tags=tag)
    print(Post)
    return render(request, 'SubjectTags/post_list_by_tag.html', {'posts': posts, 'tag': tag})

def blogs_list_by_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    blogs = URLsub.objects.filter(tags=tag)
    print(blogs)
    return render(request, 'SubjectTags/blogs_list_by_tag.html', {'blogs': blogs, 'tag': tag})
