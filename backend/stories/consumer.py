import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger(__name__)

class StoryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"WebSocket CONNECT requested for channel {self.channel_name}")
        auth = JWTAuthentication()
        try:
            logger.debug(f"Attempting JWT authentication with headers: {self.scope.get('headers')}")
            validated_token = auth.get_validated_token(self.scope["headers"])
            user, _ = auth.get_user(validated_token)
            self.user_id = user.id
            self.room_group_name = f"story_user_{self.user_id}"
            logger.info(f"User {self.user_id} authenticated. Joining group {self.room_group_name}")
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            logger.info(f"WebSocket CONNECTED for user {self.user_id} on channel {self.channel_name}")
        except Exception as e:
            logger.error(f"WebSocket CONNECT error for channel {self.channel_name}: {e}", exc_info=True)
            await self.close()
            logger.info(f"WebSocket CONNECTION CLOSED due to error for channel {self.channel_name}")

    async def disconnect(self, close_code):
        logger.info(f"WebSocket DISCONNECT requested for channel {self.channel_name} with close code: {close_code}")
        if hasattr(self, 'room_group_name'):
            logger.info(f"User {self.user_id} leaving group {self.room_group_name}")
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"User {self.user_id} removed from group {self.room_group_name}")
        logger.info(f"WebSocket DISCONNECTED for channel {self.channel_name}")

    async def story_send(self, event):
        story = event['story']
        logger.debug(f"Received 'story_send' event: {event}")
        try:
            await self.send(text_data=json.dumps({'story': story}))
            logger.info(f"Sent story update to channel {self.channel_name}: {story}")
        except Exception as e:
            logger.error(f"Error sending story update to channel {self.channel_name}: {e}", exc_info=True)

    async def user_joined(self, event):
        user_id = event['user_id']
        logger.info(f"Received 'user_joined' event for user {user_id}")
        try:
            await self.send(text_data=json.dumps({'type': 'user_joined', 'user_id': user_id}))
            logger.info(f"Sent 'user_joined' notification to channel {self.channel_name} for user {user_id}")
        except Exception as e:
            logger.error(f"Error sending 'user_joined' notification to channel {self.channel_name}: {e}", exc_info=True)

    async def user_left(self, event):
        user_id = event['user_id']
        logger.info(f"Received 'user_left' event for user {user_id}")
        try:
            await self.send(text_data=json.dumps({'type': 'user_left', 'user_id': user_id}))
            logger.info(f"Sent 'user_left' notification to channel {self.channel_name} for user {user_id}")
        except Exception as e:
            logger.error(f"Error sending 'user_left' notification to channel {self.channel_name}: {e}", exc_info=True)

    async def story_updated(self, event):
        story_data = event['story_data']
        logger.info(f"Received 'story_updated' event: {story_data}")
        try:
            await self.send(text_data=json.dumps({'type': 'story_updated', 'story': story_data}))
            logger.info(f"Sent 'story_updated' notification to channel {self.channel_name}: {story_data}")
        except Exception as e:
            logger.error(f"Error sending 'story_updated' notification to channel {self.channel_name}: {e}", exc_info=True)

    async def story_deleted(self, event):
        story_id = event['story_id']
        logger.info(f"Received 'story_deleted' event for story ID: {story_id}")
        try:
            await self.send(text_data=json.dumps({'type': 'story_deleted', 'story_id': story_id}))
            logger.info(f"Sent 'story_deleted' notification to channel {self.channel_name} for story ID: {story_id}")
        except Exception as e:
            logger.error(f"Error sending 'story_deleted' notification to channel {self.channel_name}: {e}", exc_info=True)