from message_library import message_library
from message import Message
from controller import Controller
import decorators
import subprocess

class Lobby(Controller):
    def __init__(self, network_obj, **kwargs):
        super().__init__(network_obj, **kwargs)
        self.last_player_id = 0
        self.last_game_id = 0
        self.game_id_step = int(kwargs['game_id_step'])
        self.lobby_id = 121
        self.active_players = {}
        self.active_games = {}

    def generate_player_id(self, message):
        next_player_id = self.gen_new_player_id()
        self.last_player_id = next_player_id
        print(next_player_id)
        self.active_players[next_player_id] = {
            'player_alias':message.payload['player_alias'],
            'player_address':message.payload['origin']
            }
        self.last_message_id+=1
        self.network_obj.enque(Message({
            'player_id':next_player_id,
            'response_to':message.m_uid(),
            'destination':tuple(message.payload['origin']),
            'origin':self.network_obj.address,
            'message_type':'set_player_id',
            'message_id':self.last_message_id,
            # 'response_to':message.m_uid(),
            'sender_id':self.sender_id()
            }))
        return next_player_id

    def start_new_game(self, message):
        # https://docs.python.org/3/library/subprocess.html
        # will likely be relevant
        #subprocess.Popen

        # initiate new game server
        new_game_id = self.generate_game_id()
        address = list(self.network_obj.address)
        address[1]+=new_game_id
        subprocess.Popen(
            ['python3','run_game.py',
            address[0], str(address[1]), str(new_game_id)]
            )

        # enque game server assignment message to founder
        self.last_message_id+=1
        self.network_obj.enque(Message({
            'destination':tuple(message.payload['origin']),
            'origin':self.network_obj.address,
            'game_address':address,
            'game_id':new_game_id,
            'response_to':message.m_uid(),
            'message_type':'game_assignment',
            'sender_id':self.sender_id(),
            'message_id':self.last_message_id
            }))
        return new_game_id

    def generate_game_id(self):
        next_game_id = self.last_game_id+self.game_id_step
        if next_game_id == self.lobby_id:
            next_game_id+= self.game_id_step
        self.active_games[next] = {'players':[]}
        self.last_game_id = next_game_id
        return next_game_id

    def gen_new_player_id(self):
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
        return next_player_id

    def sender_id(self):
        return self.lobby_id
