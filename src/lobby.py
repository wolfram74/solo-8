from message_library import message_library
from message import Message

class Lobby:
    def __init__(self, network_obj, **kwargs):
        self.network_obj = network_obj
        self.last_player_id = 0
        self.last_game_id = 0
        self.game_id_step = int(kwargs['game_id_step'])
        self.lobby_id = 121
        self.active_players = {}
        self.active_games = {}

    def generate_player_id(self, message):
        next_player_id = self.last_player_id+1
        valid = False
        while not valid:
            game_col = True
            lob_col = True
            if not next_player_id%self.game_id_step==0:
                game_col = False
            else:
                next_player_id+=1
            if not next_player_id == self.lobby_id:
                lob_col = False
            else:
                next_player_id += 1
            valid = (not game_col) and (not lob_col)
        self.last_player_id = next_player_id
        self.active_players[next_player_id] = {
            'player_alias':message.payload['player_alias'],
            'player_address':message.payload['origin']
            }
        self.network_obj.enque(Message({
            'destination':tuple(message.payload['origin']),
            'origin':self.network_obj.address,
            'message_id':'set_player_id',
            'player_id':next_player_id,
            }))
        return next_player_id

    def generate_game_id(self):
        next_game_id = self.last_game_id+self.game_id_step
        if next_game_id == self.lobby_id:
            next_game_id+= self.game_id_step
        self.active_games[next] = {'players':[]}
        self.last_game_id = next_game_id
        return next_game_id

    def sender_id(self):
        return self.lobby_id
