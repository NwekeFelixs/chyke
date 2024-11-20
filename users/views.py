from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserProfileSerializer
from django.contrib.auth import get_user_model
from post.models import Post
from rest_framework import generics, permissions, status
from post.serializers import PostSerializer

User = get_user_model()

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        try:
            user = User.objects.get(id=user_id) if user_id else request.user
            profile_serializer = UserProfileSerializer(user)
            posts = Post.objects.filter(user=user).order_by('-created_at')
            post_serializer = PostSerializer(posts, many=True)
            
            response_data = {
                "profile": profile_serializer.data,
                "posts": post_serializer.data,
            }

            # Log the data for debugging
            print(response_data)  # <-- Add this line for logging

            return Response(response_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
