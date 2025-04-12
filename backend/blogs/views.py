from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    """Registers a new user"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to register a new user.")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"New user registered with username: {user.username} and ID: {user.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"User registration failed due to invalid data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(generics.GenericAPIView):
    """Logs in a user and returns JWT token"""
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info("Attempting user login.")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.validated_data
            logger.info(f"User '{response_data.get('username', 'unknown')}' logged in successfully. Returning JWT.")
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            logger.warning(f"User login failed due to invalid credentials: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)