from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from friends.models import Friendship

# Create Post API
class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]  # Add these parsers to handle file uploads

    def get_queryset(self):
        # Filter posts by the logged-in user if they are authenticated
        if self.request.user.is_authenticated:
            return Post.objects.all().order_by('-created_at')
        return Post.objects.all().order_by('-created_at')  # Public posts for unauthenticated users

    def perform_create(self, serializer):
        # Assign the current user to the post when it is created
        serializer.save(user=self.request.user)

# Create Comment API
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(user=self.request.user, post=post)

# Like API
class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)
        return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)

# Feed API
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Get friendships where the status is "accepted"
        friendships = Friendship.objects.filter(
            Q(sender=user, status="accepted") | Q(receiver=user, status="accepted")
        )

        # Get friend IDs
        friend_ids = set(
            friendships.values_list("sender_id", flat=True)
        ) | set(friendships.values_list("receiver_id", flat=True))
        friend_ids.discard(user.id)  # Exclude self from friend list

        # Get posts from the user and their friends
        return Post.objects.filter(Q(user=user) | Q(user__id__in=friend_ids)).order_by('-created_at')

# User Profile Posts API
