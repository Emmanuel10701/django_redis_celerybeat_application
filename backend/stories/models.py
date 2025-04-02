from django.db import models
from django.conf import settings  # Import settings
from django.utils import timezone

class StorySchedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL
    scheduled_time = models.DateTimeField()
    preferences = models.JSONField(null=True, blank=True)
    story_generated = models.BooleanField(default=False)
    story_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)