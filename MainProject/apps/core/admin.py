# core/admin.py
from django.contrib import admin
from .models import Post, Tag, BlogFullRecommend

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'updated_on')
    list_filter = ('tags', 'created_on', 'updated_on')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)} # this create the slug field from the title field
    

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