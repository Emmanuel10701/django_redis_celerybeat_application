from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import StorySchedule  # Use StorySchedule
from .serializers import StoryScheduleSerializer
from .tasks import generate_and_send_story
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = StorySchedule.objects.all()
    serializer_class = StoryScheduleSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        logger.info(f"User {request.user.id} requested a list of StorySchedules.")
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user))
        serializer = self.get_serializer(queryset, many=True)
        logger.debug(f"Retrieved StorySchedules for user {request.user.id}: {serializer.data}")
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"User {request.user.id} requested details for StorySchedule ID: {instance.id}")
        if instance.user != request.user:
            logger.warning(f"User {request.user.id} attempted to access StorySchedule ID {instance.id} belonging to another user.")
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        logger.debug(f"Retrieved StorySchedule details for ID {instance.id}: {serializer.data}")
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info(f"User {request.user.id} attempting to create a new StorySchedule.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f"StorySchedule created successfully for user {request.user.id} with ID: {serializer.instance.id}, scheduled for: {serializer.instance.scheduled_time}")

        if serializer.instance.scheduled_time <= timezone.now():
            logger.info(f"Scheduled time for StorySchedule ID {serializer.instance.id} is in the past or present. Dispatching generate_and_send_story task.")
            generate_and_send_story.delay(serializer.instance.id)
        else:
            logger.info(f"StorySchedule ID {serializer.instance.id} scheduled for {serializer.instance.scheduled_time}. Task will be triggered later.")

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.debug(f"StorySchedule saved to database for user {self.request.user.id}.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        logger.info(f"User {request.user.id} attempting to update StorySchedule ID: {instance.id}.")
        if instance.user != request.user:
            logger.warning(f"User {request.user.id} attempted to update StorySchedule ID {instance.id} belonging to another user.")
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info(f"StorySchedule ID {instance.id} updated successfully by user {request.user.id}.")

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
        logger.debug(f"StorySchedule ID {serializer.instance.id} updated in the database.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.warning(f"User {request.user.id} attempting to delete StorySchedule ID: {instance.id}.")
        if instance.user != request.user:
            logger.warning(f"User {request.user.id} attempted to delete StorySchedule ID {instance.id} belonging to another user.")
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        logger.info(f"StorySchedule ID {instance.id} deleted successfully by user {request.user.id}.")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        logger.debug(f"StorySchedule ID {instance.id} deleted from the database.")
        instance.delete()

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import razorpay
from django.conf import settings

class RazorpayPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Extract payment details from the request
            amount = request.data.get('amount')  # Amount in paise (e.g., 50000 for ₹500)
            currency = request.data.get('currency', 'INR')
            receipt = request.data.get('receipt', 'receipt#1')

            # Create an order
            order_data = {
                'amount': amount,
                'currency': currency,
                'receipt': receipt,
            }
            order = client.order.create(data=order_data)

            # Return the order details
            return Response(order, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)