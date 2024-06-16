import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from users.models import CustomUser
from channels.generic.websocket import WebsocketConsumer

def send_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'send_notification',
            'message': message
        }
    )

class NotiConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'notifications'
        # Join the group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print("WebSocket connection established.")

    def disconnect(self, close_code):
        # Leave the group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket connection closed with code: {close_code}")

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        print(f"Received message: {message}")

        # Broadcast message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_notification(self, message):
        self.send(text_data=json.dumps({
            'message': message
        }))
        print(f"Sent notification: {message}")

    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
        print(f"Sent response: {message}")

def notify_winner():
    winner = CustomUser.objects.filter(winner=True).first()
    if winner:
        message = f"Global Sign-In Count Reached 5! Winner: {winner.username}"
        send_notification(message)

def notify_global_sign_in_count(count):
    message = f"{count}"
    print(message)
    send_notification(message)
