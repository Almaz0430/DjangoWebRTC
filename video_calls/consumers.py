import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, RoomMember
from asgiref.sync import sync_to_async

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'video_room_{self.room_id}'
        self.user = self.scope["user"]

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
        
        # Notify others that user has left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'user': self.user.username
            }
        )
        
        # Update user connection status
        await self.update_member_status(False)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'join':
            # Notify others about new user
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.username
                }
            )
        
        elif message_type == 'offer':
            # Handle WebRTC offer
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_offer',
                    'offer': data['offer'],
                    'sender': self.user.username,
                    'target': data.get('target')
                }
            )
        
        elif message_type == 'answer':
            # Handle WebRTC answer
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_answer',
                    'answer': data['answer'],
                    'sender': self.user.username,
                    'target': data.get('target')
                }
            )
        
        elif message_type == 'ice':
            # Handle ICE candidate
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_ice',
                    'ice': data['ice'],
                    'sender': self.user.username,
                    'target': data.get('target')
                }
            )

    async def user_join(self, event):
        await self.send(text_data=json.dumps({
            'type': 'join',
            'user': event['user']
        }))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps({
            'type': 'leave',
            'user': event['user']
        }))

    async def webrtc_offer(self, event):
        # Send offer only to target user
        if self.user.username == event['target']:
            await self.send(text_data=json.dumps({
                'type': 'offer',
                'offer': event['offer'],
                'sender': event['sender']
            }))

    async def webrtc_answer(self, event):
        # Send answer only to target user
        if self.user.username == event['target']:
            await self.send(text_data=json.dumps({
                'type': 'answer',
                'answer': event['answer'],
                'sender': event['sender']
            }))

    async def webrtc_ice(self, event):
        # Send ICE candidate only to target user
        if self.user.username == event['target']:
            await self.send(text_data=json.dumps({
                'type': 'ice',
                'ice': event['ice'],
                'sender': event['sender']
            }))

    @database_sync_to_async
    def update_member_status(self, is_connected):
        try:
            member = RoomMember.objects.get(
                room__id=self.room_id,
                user=self.user
            )
            member.is_connected = is_connected
            member.save()
        except RoomMember.DoesNotExist:
            pass 