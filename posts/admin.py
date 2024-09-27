from django.contrib import admin
from .models import Post, Resource


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['content']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    def short_content(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content

    short_content.short_description = 'Short Content'
    list_display = ['user', 'short_content', 'audience']
