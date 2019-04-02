from message_library import message_library
from message import Message
import time
import decorators

class Player:
    def __init__(self, network_obj, lobby_address, player_alias='farts'):
        self.network_obj = network_obj
        self.last_message_id = 0
        self.lobby_address = lobby_address
        self.player_alias = player_alias
        self.player_id = 0

    def request_player_id(self):
        self.last_message_id+=1
        message = Message({
            'message_type':'generate_player_id',
            'player_alias': self.player_alias,
            'destination':self.lobby_address,
            'message_id':self.last_message_id,
            'sender_id':self.sender_id()
            })
        self.network_obj.enque(message)

    def request_new_game(self):
        self.last_message_id+=1
        message = Message({
            'message_type':'start_new_game',
            'player_id':self.player_id,
            'player_alias':self.player_alias,
            'destination':self.lobby_address,
            'origin':self.network_obj.address,
            'sender_id':self.sender_id(),
            'message_id':self.last_message_id
            })
        self.network_obj.enque(message)

    def game_assignment(self, message):
        self.game_id = message.payload['game_id']
        self.game_address = message.payload['game_address']
        self.send_ack(message)
        self.request_join_game()

    def request_join_game(self):
        #is sensitive to timing
        self.last_message_id+=1
        message = Message({
            'message_type':'add_new_player',
            'player_id':self.player_id,
            'player_alias':self.player_alias,
            'destination':self.game_address,
            'origin':self.network_obj.address,
            'sender_id':self.sender_id(),
            'message_id':self.last_message_id
            })
        print(message.payload)
        # time.sleep(.5)
        self.network_obj.enque(message)

    def set_player_id(self, message):
        self.player_id = message.payload['player_id']
        if self.network_obj.address == None:
            self.network_obj.address = message.payload['destination']
        self.send_ack(message)
        return self.player_id

    def sender_id(self):
        return self.player_id

    def ack(self, message):
        print('coolio')

    @decorators.route
    def send_ack(self, message):
        # print('ack:',message.payload)
        out_bound={
        'response_to':message.m_uid(),
        'destination':message.payload['origin'],
        'message_type':'ack'
        }
        return Message(payload=out_bound, persist=False)
