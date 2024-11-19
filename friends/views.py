from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Friendship
from .serializers import FriendshipSerializer
from django.contrib.auth import get_user_model
from story.serializers import StorySerializer
from story.models import Story

User = get_user_model()

class FriendRequestView(APIView):
    def post(self, request, *args, **kwargs):
        receiver_id = request.data.get("receiver_id")
        receiver = User.objects.get(pk=receiver_id)

        # Check if the request already exists
        if Friendship.objects.filter(sender=request.user, receiver=receiver).exists():
            return Response({"detail": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)

        friendship = Friendship.objects.create(sender=request.user, receiver=receiver)
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AcceptFriendRequestView(APIView):
    def post(self, request, *args, **kwargs):
        request_id = kwargs.get("pk")
        try:
            friendship = Friendship.objects.get(pk=request_id, receiver=request.user, status="pending")
            friendship.status = "accepted"
            friendship.save()
            return Response({"detail": "Friend request accepted."}, status=status.HTTP_200_OK)
        except Friendship.DoesNotExist:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)


class RejectFriendRequestView(APIView):
    def post(self, request, *args, **kwargs):
        request_id = kwargs.get("pk")
        try:
            friendship = Friendship.objects.get(pk=request_id, receiver=request.user, status="pending")
            friendship.status = "rejected"
            friendship.save()
            return Response({"detail": "Friend request rejected."}, status=status.HTTP_200_OK)
        except Friendship.DoesNotExist:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)


class FriendStoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Retrieve friends with accepted status
        friendships = Friendship.objects.filter(
            (models.Q(sender=user) | models.Q(receiver=user)),
            status="accepted"
        )

        # Get the users who are friends
        friend_ids = [friendship.receiver.id if friendship.sender == user else friendship.sender.id for friendship in friendships]

        # Retrieve the most recent stories for those friends (limit to 5)
        recent_stories = Story.objects.filter(user__id__in=friend_ids).order_by('-created_at')[:5]

        # Serialize the stories
        serializer = StorySerializer(recent_stories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)