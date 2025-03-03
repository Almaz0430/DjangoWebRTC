import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, RoomMember

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'video_room_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Update user connection status
        if hasattr(self, 'user'):
            await self.update_member_status(False)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'offer':
            # Handle WebRTC offer
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_offer',
                    'offer': data['offer'],
                    'sender_channel_name': self.channel_name,
                }
            )
        elif message_type == 'answer':
            # Handle WebRTC answer
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_answer',
                    'answer': data['answer'],
                    'sender_channel_name': self.channel_name,
                }
            )
        elif message_type == 'ice':
            # Handle ICE candidate
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_ice',
                    'ice': data['ice'],
                    'sender_channel_name': self.channel_name,
                }
            )

    async def webrtc_offer(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'type': 'offer',
                'offer': event['offer']
            }))

    async def webrtc_answer(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'type': 'answer',
                'answer': event['answer']
            }))

    async def webrtc_ice(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'type': 'ice',
                'ice': event['ice']
            }))

    @database_sync_to_async
    def update_member_status(self, is_connected):
        try:
            member = RoomMember.objects.get(
                room__id=self.room_id,
                user=self.scope['user']
            )
            member.is_connected = is_connected
            member.save()
        except RoomMember.DoesNotExist:
            pass 