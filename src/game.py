from message import Message

class Game():
    def __init__(self, network_obj, **kwargs):
        self.network_obj = network_obj
        self.game_id = kwargs['game_id']
        self.active_players = {}
        self.secret_word = ''
        self.chars_revealed = 0
        self.last_clue_id = 0
        self.active_clues = {}
        self.contacted_clue = 0

    def add_new_player(self, message):
        new_id = message.payload['player_id']
        new_alias = message.payload['player_alias']
        new_address = message.payload['origin']
        self.active_players[new_id] = {
            'player_alias': new_alias,
            'player_address': new_address,
        }
        self.update_bulk_state(new_id)

    def update_bulk_state(self, player_id):
        #we'll get to it after figuring out remote IP addressing
        pass
