# orders/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'order_{self.order_id}'

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

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        status = data.get('status')

        # Broadcast status to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'order_status',
                'status': status
            }
        )

    # Receive message from group
    async def order_status(self, event):
        status = event['status']
        await self.send(text_data=json.dumps({
            'status': status
        }))
