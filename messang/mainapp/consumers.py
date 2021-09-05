import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, User

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.get_30_messages()
        lst_of_messages = self.messages_to_json(messages)
        content = {
            'command': 'fetch_messages',
            'messages': lst_of_messages
        }
        self.send_message(content)
        

    def new_message(self, data):
        author = data.get('author', None)
        content = data.get('message', None)
        if author is None:
            return False
        author_user = User.objects.filter(username=author).first()
        if not author_user:
            return False
        message = Message.objects.create(
            author=author_user,
            content=content
        )
        context = {
            'message': self.to_json(message),
            'command': 'new_message'
        }
        return self.send_chat_message(context)


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def messages_to_json(self, messages):
        lst_of_messages = []
        for message in messages:
            lst_of_messages.append(self.to_json(message))
        return lst_of_messages


    def to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'date': str(message.date),
        }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.commands[text_data_json['command']](self, text_data_json)


    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message
            }
        )
    
    def send_message(self, message):
        self.send(text_data=json.dumps(message))
    
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))