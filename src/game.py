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
