from message_library import message_library
from message import Message

class Player:
    def __init__(self, network_obj, lobby_address, player_alias='farts'):
        self.network_obj = network_obj
        self.lobby_address = lobby_address
        self.player_alias = player_alias
        self.last_message_id = 0

    def request_player_id(self):
        message = Message({
            'message_type':'generate_player_id',
            'player_alias': self.player_alias,
            'destination':self.lobby_address,
            'origin':self.network_obj.address
            })
        self.network_obj.enque(message)

    def request_new_game(self):
        self.last_message_id+=1
        message = Message({
            'message_type':'start_new_game',
            'player_id':self.player_id,
            'sender_id':self.sender_id()
            'message_id':self.sender_id()
            })

    def set_player_id(self, message):
        self.player_id = message.payload['player_id']
        return self.player_id

    def sender_id(self):
        return self.player_id
