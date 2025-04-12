from django.db import models
from django.conf import settings  # Import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class StorySchedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL
    scheduled_time = models.DateTimeField()
    preferences = models.JSONField(null=True, blank=True)
    story_generated = models.BooleanField(default=False)
    story_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"New StorySchedule created for user: {self.user.username}, scheduled for: {self.scheduled_time}")
        else:
            logger.info(f"StorySchedule updated (ID: {self.id}) for user: {self.user.username}, scheduled for: {self.scheduled_time}")

    def delete(self, *args, **kwargs):
        logger.warning(f"StorySchedule deleted (ID: {self.id}) for user: {self.user.username}, scheduled for: {self.scheduled_time}")
        super().delete(*args, **kwargs)