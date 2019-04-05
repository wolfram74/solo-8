import decorators
import subprocess
import sys
import configparser
from message import Message
from network_io import NetworkIO
from controller import Controller

class Lobby(Controller):
    def __init__(self, network_obj, **kwargs):
        super().__init__(network_obj, **kwargs)
        self.last_player_id = 0
        self.last_game_id = 0
        self.game_id_step = int(kwargs['game_id_step'])
        self.lobby_id = 121
        self.active_players = {}
        self.active_games = {}

    @decorators.route
    def generate_player_id(self, message):
        next_player_id = self.gen_new_player_id()
        self.last_player_id = next_player_id
        # print(next_player_id)
        self.active_players[next_player_id] = {
            'player_alias':message.payload['player_alias'],
            'player_address':message.payload['origin']
            }
        outbound = Message({
            'response_to':message.m_uid(),
            'destination':tuple(message.payload['origin']),
            'player_id':next_player_id,
            'message_type':'set_player_id',
            })
        return outbound

    @decorators.route
    def start_new_game(self, message):
        # https://docs.python.org/3/library/subprocess.html
        # will likely be relevant
        #subprocess.Popen

        # initiate new game server
        new_game_id = self.generate_game_id()
        address = list(self.network_obj.address)
        address[1]+=new_game_id
        subprocess.Popen(
            ['python3','game.py',
            address[0], str(address[1]), str(new_game_id)]
            )

        # enque game server assignment message to founder
        outbound = Message({
            'destination':tuple(message.payload['origin']),
            'game_address':address,
            'game_id':new_game_id,
            'response_to':message.m_uid(),
            'message_type':'game_assignment',
            })
        return outbound

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


    @classmethod
    def set_up_controller(cls):
        mode = 'DEV'
        if len(sys.argv)>1 and sys.argv[1]=='PROD':
            mode = sys.argv[1]

        config = configparser.ConfigParser()
        config.read('config.ini')

        connection = NetworkIO((
            config[mode]['lobby_ip'],
            int(config[mode]['lobby_port'])
        ))
        return Lobby(connection, **config[mode])

if __name__ == '__main__':
    lobby = Lobby.set_up_controller()
    while True:
        lobby.primary_loop()
