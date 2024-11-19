from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'created_by', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    list_filter = ('is_public', 'created_by')
    ordering = ('-created_at',)

admin.site.register(Event, EventAdmin)
