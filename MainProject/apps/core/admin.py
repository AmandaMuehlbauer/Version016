# core/admin.py
from django.contrib import admin
from .models import Post, Tag, BlogFullRecommend, Comment



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'updated_on', 'display_tags')
    list_filter = ('tags', 'created_on', 'updated_on')
    search_fields = ('title','tags__name')
    prepopulated_fields = {'slug': ('title',)} # this create the slug field from the title field
    autocomplete_fields = ('tags',)


    # Define a custom method to display tags as a string
    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    display_tags.short_description = "Tags" # Set a custom column header

admin.site.register(Post, PostAdmin)

# TagAdmin must define "search_fields", because it's referenced by PostAdmin.autocomplete_fields.
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Tag, TagAdmin)


class BlogFullRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'author', 'last_updated')
    list_filter = ('author', 'last_updated')
    search_fields = ('title', 'content')

admin.site.register(BlogFullRecommend, BlogFullRecommendAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created')
    list_filter = ('created', 'post')
    search_fields = ('author__username', 'post__title', 'content')
    date_hierarchy = 'created'

admin.site.register(Comment, CommentAdmin)