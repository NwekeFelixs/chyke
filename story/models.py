from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="stories/images/", blank=True, null=True)
    video = models.FileField(upload_to="stories/videos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Ensure only one field is filled (content, image, or video)
        if sum(bool(field) for field in [self.content, self.image, self.video]) > 1:
            raise ValidationError("You can only provide one of content, image, or video.")
