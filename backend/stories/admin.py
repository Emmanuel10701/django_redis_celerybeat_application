from django.contrib import admin
from .models import StorySchedule

class StoryScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'scheduled_time', 'preferences') # removed title and created_at.
    list_filter = ('scheduled_time',) # removed created_at.
    ordering = ('scheduled_time',) # removed created_at.

admin.site.register(StorySchedule, StoryScheduleAdmin)