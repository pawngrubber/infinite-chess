import json
from channels.generic.websocket import AsyncWebsocketConsumer
from uuid import uuid4
from board.board import Board, Color, Move
from board.logic import Coordinate

# Global state for matchmaking and games (In-memory for simplicity)
waiting_players = []
active_games = {} # game_id -> Board instance

class MatchmakingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.player_id = str(uuid4())
        self.game_id = None
        self.color = None
        await self.accept()
        
        # Add player to the queue
        waiting_players.append(self)
        
        # If we have two or more players, pair them up
        if len(waiting_players) >= 2:
            p1 = waiting_players.pop(0)
            p2 = waiting_players.pop(0)
            
            game_id = f"game_{uuid4()}"
            
            # Initialize board
            board = Board()
            board.setup_board()
            active_games[game_id] = board
            
            # Notify both players they are matched
            await p1.set_game(game_id, 'WHITE', board.to_dict())
            await p2.set_game(game_id, 'BLACK', board.to_dict())
            
    async def set_game(self, game_id, color, board_state):
        self.game_id = game_id
        self.color = color
        await self.channel_layer.group_add(game_id, self.channel_name)
        await self.send(text_data=json.dumps({
            'type': 'matched',
            'game_id': game_id,
            'color': color,
            'board': board_state
        }))

    async def disconnect(self, close_code):
        if self in waiting_players:
            waiting_players.remove(self)
        if self.game_id:
            await self.channel_layer.group_discard(self.game_id, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data.get('type') == 'move':
            game_id = data.get('game_id')
            board = active_games.get(game_id)
            
            if not board:
                return

            # Validate turn
            if board.turn.name != self.color:
                await self.send(text_data=json.dumps({'type': 'error', 'message': 'Not your turn'}))
                return

            # Parse move
            try:
                start = Coordinate.from_dict(data['move']['start'])
                end = Coordinate.from_dict(data['move']['end'])
                # Find the legal move in the board's legal moves
                legal_moves = board.get_legal_moves(start)
                move_to_apply = next((m for m in legal_moves if m.end == end), None)
                
                if move_to_apply:
                    new_board = board.make_move(move_to_apply)
                    active_games[game_id] = new_board
                    
                    # Broadcast update
                    await self.channel_layer.group_send(
                        game_id,
                        {
                            'type': 'game_update',
                            'board': new_board.to_dict(),
                            'last_move': data['move']
                        }
                    )
                else:
                    await self.send(text_data=json.dumps({'type': 'error', 'message': 'Illegal move'}))
            except Exception as e:
                await self.send(text_data=json.dumps({'type': 'error', 'message': str(e)}))

    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'update',
            'board': event['board'],
            'last_move': event.get('last_move')
        }))
