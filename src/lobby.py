from message_library import message_library

class Lobby:
    def __init__(self, network_obj):
        self.network_obj = network_obj

    def generate_player_id(self, message):
        print(message.payload)
