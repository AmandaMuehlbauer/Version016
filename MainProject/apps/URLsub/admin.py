#apps/URLsub/admin.py
from django.contrib import admin
from .models import URLsub
# Register your models here.



class URLsubAdmin(admin.ModelAdmin):
    list_display = ('username', 'description', 'tags', 'url', 'timestamp')
    list_filter = ('username', 'tags')
    search_fields = ('username__username', 'description', 'tags__name', 'url')
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('User Info', {'fields': ('username',)}),
        ('URL Info', {'fields': ('description', 'tags', 'url')}),
    )

    filter_horizontal = ('tags',)
    readonly_fields = ('timestamp',)  # Add this line to mark 'timestamp' as read-only

admin.site.register(URLsub, URLsubAdmin)