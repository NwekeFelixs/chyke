from django.conf import settings
from django.db import models

from django.core.exceptions import ValidationError

class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
    )
    content = models.TextField(blank=True, null=True)  # Make content optional
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Adding validation to ensure valid combinations
    def clean(self):
        # Ensure a post has at least one of content, image, or video
        if not self.content and not self.image and not self.video:
            raise ValidationError("A post must have at least one of content, image, or video.")
        
        # Ensure a post does not have both an image and a video
        if self.image and self.video:
            raise ValidationError("A post cannot have both an image and a video.")

    def save(self, *args, **kwargs):
        self.full_clean()  # This calls the clean method before saving the post
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post by {self.user} - {self.created_at}"

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()

class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user} liked {self.post.id}"

class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post.id}"
