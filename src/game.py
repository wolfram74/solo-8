from message import Message
import decorators

class Game():
    def __init__(self, network_obj, **kwargs):
        self.network_obj = network_obj
        self.game_id = kwargs['game_id']
        self.active_players = {}
        self.secret_word = ''
        self.chars_revealed = 0
        self.last_clue_id = 0
        self.last_message_id = 0
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
        self.send_ack(message)
        self.update_bulk_state(new_id)

    def update_bulk_state(self, player_id):
        #we'll get to it after figuring out remote IP addressing
        pass

    def sender_id(self):
        return self.game_id

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
