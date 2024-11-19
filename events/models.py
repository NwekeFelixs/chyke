from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()  # Calendar-style date
    time = models.TimeField(blank=True, null=True)  # Optional time
    duration = models.DurationField(null=True, blank=True)  # Optional event duration
    location = models.CharField(max_length=255, null=True, blank=True)  # Event location
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="created_events"
    )
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="attending_events", blank=True)  # Track attendees
    category = models.CharField(max_length=50, choices=[
        ('Music', 'Music'),
        ('Sports', 'Sports'),
        ('Seminars', 'Seminars'),
    ], null=True, blank=True)  # Optional event category
    is_public = models.BooleanField(default=False)  # Public/Private event
    recurrence = models.CharField(max_length=50, choices=[
        ('None', 'None'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    ], default='None')  # Recurrence rules
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.date}"
