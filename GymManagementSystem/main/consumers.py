from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name='noti_group_name'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        self.accept()
        self.send(text_data="Group created")
    
    def receive(self, text_data=None):
        self.send(text_data="Hello World!")
    
    def disconnect(self, close_code):
        self.close(close_code)