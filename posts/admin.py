from django.contrib import admin
from .models import Post
from django.contrib.auth.models import User

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['content']
