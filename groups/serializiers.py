from rest_framework import serializers
from .models import Group, GroupMembership

class GroupSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'created_by', 'members')
        read_only_fields = ('created_by', 'members')

class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = ('id', 'user', 'group', 'joined_at')
        read_only_fields = ('joined_at',)
