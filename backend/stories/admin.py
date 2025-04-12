from django.contrib import admin
from .models import StorySchedule
import logging

logger = logging.getLogger(__name__)

class StoryScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'scheduled_time', 'preferences') # removed title and created_at.
    list_filter = ('scheduled_time',) # removed created_at.
    ordering = ('scheduled_time',) # removed created_at.

    def save_model(self, request, obj, form, change):
        logger.info(f"Saving StorySchedule object for user: {obj.user.username}, scheduled time: {obj.scheduled_time}, preferences: {obj.preferences}")
        super().save_model(request, obj, form, change)
        logger.info(f"StorySchedule object saved with ID: {obj.id}")

    def delete_model(self, request, obj):
        logger.warning(f"Deleting StorySchedule object with ID: {obj.id}, user: {obj.user.username}, scheduled time: {obj.scheduled_time}")
        super().delete_model(request, obj)
        logger.warning(f"StorySchedule object with ID: {obj.id} deleted.")

admin.site.register(StorySchedule, StoryScheduleAdmin)