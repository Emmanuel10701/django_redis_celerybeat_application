from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import StorySchedule # Use StorySchedule
from .serilizers import StoryScheduleSerializer
from .task import generate_and_send_story
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = StorySchedule.objects.all()
    serializer_class = StoryScheduleSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if serializer.instance.scheduled_time <= timezone.now():
            generate_and_send_story.delay(serializer.instance.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)