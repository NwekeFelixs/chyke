from django.contrib import admin
from .models import Group, GroupMembership

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')
    search_fields = ('name', 'description')

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'joined_at')
    search_fields = ('user__username', 'group__name')