from django.urls import path
from .views import StoryCreateView

urlpatterns = [
    path("create-story/", StoryCreateView.as_view(), name="create-story"),
]
