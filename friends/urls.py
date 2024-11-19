from django.urls import path
from .views import FriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, FriendStoriesView

urlpatterns = [
    path("friend-requests/", FriendRequestView.as_view(), name="friend-request"),
    path("friend-requests/<int:pk>/accept/", AcceptFriendRequestView.as_view(), name="accept-friend-request"),
    path("friend-requests/<int:pk>/reject/", RejectFriendRequestView.as_view(), name="reject-friend-request"),
    path('friends/stories/', FriendStoriesView.as_view(), name='friend-stories'),

]
