from django.contrib import admin
from .models import Session, Recording


# Register your models here.

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'host', 'title', 'start_time', 'end_time', 'is_active')
    list_filter = ('host', 'start_time', 'end_time', 'is_active')
    search_fields = ('channel_name',)


@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = ('session', 'resource_id', 'sid', 'file_url', 'start_time', 'end_time', 'duration')
    list_filter = ('session', 'start_time', 'end_time')
    search_fields = ('session__channel_name',)
