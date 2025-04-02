import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.authentication import JWTAuthentication

class StoryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        auth = JWTAuthentication()
        try:
            validated_token = auth.get_validated_token(self.scope["headers"])
            user, _ = auth.get_user(validated_token)
            self.user_id = user.id
            self.room_group_name = f"story_user_{self.user_id}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            print(f"WebSocket connect error: {e}")
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def story_send(self, event):
        story = event['story']
        await self.send(text_data=json.dumps({'story': story}))