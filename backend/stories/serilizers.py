from rest_framework import serializers
from .models import StorySchedule

class StoryScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorySchedule
        fields = ['id', 'scheduled_time', 'preferences']