import json
from channels.generic.websocket import AsyncWebsocketConsumer
from uuid import uuid4

# Global queue for matchmaking (In-memory for simplicity)
waiting_players = []

class MatchmakingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.player_id = str(uuid4())
        await self.accept()
        
        # Add player to the queue
        waiting_players.append(self)
        
        # If we have two or more players, pair them up
        if len(waiting_players) >= 2:
            p1 = waiting_players.pop(0)
            p2 = waiting_players.pop(0)
            
            game_room = f"game_{uuid4()}"
            
            # Notify both players they are matched
            await p1.send(text_data=json.dumps({
                'type': 'matched',
                'room': game_room,
                'color': 'white'
            }))
            await p2.send(text_data=json.dumps({
                'type': 'matched',
                'room': game_room,
                'color': 'black'
            }))
            
            # Join the room (Simplified for now)
            await p1.channel_layer.group_add(game_room, p1.channel_name)
            await p2.channel_layer.group_add(game_room, p2.channel_name)
            
    async def disconnect(self, close_code):
        if self in waiting_players:
            waiting_players.remove(self)

    async def receive(self, text_data):
        # Forward game moves to the room
        data = json.loads(text_data)
        if 'room' in data:
            await self.channel_layer.group_send(
                data['room'],
                {
                    'type': 'game_message',
                    'message': data
                }
            )

    async def game_message(self, event):
        await self.send(text_data=json.dumps(event['message']))
