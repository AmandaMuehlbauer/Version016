#apps/URLsub/admin.py
from django.contrib import admin
from .models import URLsub
# Register your models here.



class URLsubAdmin(admin.ModelAdmin):
    list_display = ('author_username', 'author_email', 'title', 'description', 'tags_list', 'url', 'timestamp')
    list_filter = ('user','title', 'tags')
    search_fields = ('user__username','title', 'description', 'tags__name', 'url')
    date_hierarchy = 'timestamp'

    fieldsets = (
        ('User Info', {'fields': ('user',)}),
        ('URL Info', {'fields': ('title', 'description', 'tags', 'url')}),
    )

    filter_horizontal = ('tags',)
    readonly_fields = ('timestamp',)  # Mark 'timestamp' as read-only

    def author_username(self, obj):
        return obj.user.username  # Access the username of the user

    def author_email(self, obj):
        return obj.user.email  # Access the email of the user

    def tags_list(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    tags_list.short_description = "Tags"

admin.site.register(URLsub, URLsubAdmin)