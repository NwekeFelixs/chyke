from rest_framework import serializers
from .models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')  # Get the username
    profile_picture = serializers.SerializerMethodField()  # Custom field for profile picture

    class Meta:
        model = Post
        fields = [
            'id', 'content', 'image', 'created_at', 'username', 'profile_picture',
            'like_count', 'comment_count'
        ]

    def get_profile_picture(self, obj):
        # Return the profile picture URL; replace 'profile_picture' with the actual field name
        return obj.user.profile_picture.url if obj.user.profile_picture else None


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
