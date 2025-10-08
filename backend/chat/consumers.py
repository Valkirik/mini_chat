import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Имя комнаты (из URL, например ws/chat/lobby/)
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = f"chat_{self.room_name}"

        # Присоединяем соединение к группе
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()  # принимаем соединение

    async def disconnect(self, close_code):
        # Удаляем соединение из группы при закрытии
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Получаем сообщение от клиента
        data = json.loads(text_data)
        message = data.get("message", "")

        # Рассылаем его всем в группе
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",  # вызывает метод chat_message
                "message": message,
            }
        )

    async def chat_message(self, event):
        # Отправляем сообщение обратно клиенту
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))