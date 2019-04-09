import time
import decorators
import sys
import select
import configparser
from message_library import message_library
from message import Message
from controller import Controller
from network_io import NetworkIO

class Player(Controller):
    def __init__(self, network_obj, lobby_address, player_alias='farts', **kwargs):
        super().__init__(network_obj, **kwargs)
        self.lobby_address = lobby_address
        self.player_alias = player_alias
        self.player_id = 0
        self.game_id = None
        self.game_address = None
        self.secret_word=''
        self.visible_letters=0
        self.active_guesses = {}

    @decorators.route
    def request_player_id(self):
        message = Message({
            'message_type':'generate_player_id',
            'player_alias': self.player_alias,
            'destination':self.lobby_address,
            })
        return message

    @decorators.route
    def request_new_game(self):
        message = Message({
            'message_type':'start_new_game',
            'player_id':self.player_id,
            'player_alias':self.player_alias,
            'destination':self.lobby_address,
            })
        return message

    def game_assignment(self, message):
        self.game_id = message.payload['game_id']
        self.game_address = message.payload['game_address']
        self.send_ack(message)
        self.request_join_game(message)


    @decorators.route
    def request_join_game(self, message):
        message = Message({
            'message_type':'add_new_player',
            'player_id':self.player_id,
            'player_alias':self.player_alias,
            'destination':self.game_address,
            })
        return message

    @decorators.route
    def submit_secret_word(self, message):
        outbound = Message({
            'message_type':'distribute_secret_word',
            'secret_word':message.payload['secret_word'],
            'destination':self.game_address,
            })
        return outbound

    def receive_new_secret_word(self, message):
        self.secret_word = message.payload['secret_word']
        self.visible_letters = 1
        self.send_ack(message)

    @decorators.route
    def submit_guess(self, message):
        outbound = Message({
            'message_type':'distribute_guess',
            'guess_word':message.payload['guess_word'],
            'guess_clue':message.payload['guess_clue'],
            'destination':self.game_address,

            })
        return outbound

    def receive_new_guess(self, message):
        self.active_guesses[message.payload['guess_id']]={
            'guess_word':message.payload['guess_word'],
            'guess_clue':message.payload['guess_clue'],
            'blocks':[],
            'contacts':[]
        }
        self.send_ack(message)

    @decorators.route
    def submit_contact(self,message):
        outbound = Message({
            'message_type':'distribute_contact',
            'destination':self.game_address,
            'contact_guess':message.payload['contact_guess'],
            'guess_id':message.payload['guess_id']
            })
        return outbound

    def receive_contact_notification(self, message):
        pass

    def set_player_id(self, message):
        self.player_id = message.payload['player_id']
        # print('!!! player ID set\n')
        if self.network_obj.address == None:
            self.network_obj.address = message.payload['destination']
        self.send_ack(message)
        return self.player_id

    def sender_id(self):
        return self.player_id

    def visible_word(self):
        return self.secret_word[:self.visible_letters]

    def get_readers(self):
        readers, _, _ = select.select([self.network_obj.socket, sys.stdin], [],[],0)
        return readers

    @classmethod
    def set_up_controller(cls):
        mode = 'DEV'
        ignored_args = ['-v']
        if len(sys.argv)>1 and sys.argv[1] not in ignored_args:
            mode = sys.argv[1]

        config = configparser.ConfigParser()
        config.read('config.ini')

        connection = NetworkIO()
        lobby_address =(
            config[mode]['lobby_ip'],
            int(config[mode]['lobby_port'])
        )

        return Player(connection, lobby_address)

if __name__ == '__main__':
    player = Player.set_up_controller()
    while True:
        player.primary_loop()
