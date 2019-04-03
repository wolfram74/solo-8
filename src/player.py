from message_library import message_library
from message import Message
from controller import Controller
import time
import decorators

class Player(Controller):
    def __init__(self, network_obj, lobby_address, player_alias='farts', **kwargs):
        super().__init__(network_obj, **kwargs)
        self.lobby_address = lobby_address
        self.player_alias = player_alias
        self.player_id = 0


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

    def set_player_id(self, message):
        self.player_id = message.payload['player_id']
        if self.network_obj.address == None:
            self.network_obj.address = message.payload['destination']
        self.send_ack(message)
        return self.player_id

    def sender_id(self):
        return self.player_id
