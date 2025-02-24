import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("task_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("task_updates", self.channel_name)

    async def send_task_update(self, event):
        message = event["message"]
        new_task = event.get("new_task", None)
        
        await self.send(text_data=json.dumps({
            "message": message,
            "new_task": new_task
        }))
