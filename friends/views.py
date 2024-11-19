from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Friendship
from .serializers import FriendshipSerializer
from django.contrib.auth import get_user_model

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
