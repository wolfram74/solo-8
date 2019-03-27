from message_library import message_library
from message import Message

class Player:
    def __init__(self, network_obj, lobby_address, player_alias='farts'):
        self.network_obj = network_obj
        self.lobby_address = lobby_address
        self.player_alias = player_alias

    def request_player_id(self):
        message = Message({
            'message_id':'generate_player_id',
            'player_alias': self.player_alias,
            'destination':self.lobby_address,
            'origin':self.network_obj.address
            })
        self.network_obj.enque(message)

    def set_player_id(self, message):
        self.player_id = message.payload['player_id']
        return self.player_id
