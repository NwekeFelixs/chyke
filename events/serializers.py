from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'created_by', 'is_public', 'created_at']
