import sys
import configparser
import decorators
import select
from message import Message
from controller import Controller
from network_io import NetworkIO

class Game(Controller):
    def __init__(self, network_obj, **kwargs):
        super().__init__(network_obj, **kwargs)
        self.game_id = kwargs['game_id']
        self.active_players = {}
        self.secret_word = ''
        self.chars_revealed = 0
        self.active_guesses = {}
        self.last_guess_id = 0

    def add_new_player(self, message):
        new_id = message.payload['player_id']
        new_alias = message.payload['player_alias']
        new_address = message.payload['origin']
        self.active_players[new_id] = {
            'player_alias': new_alias,
            'player_address': new_address,
        }
        self.send_ack(message)
        # self.update_bulk_state(message)

    @decorators.route
    def update_bulk_state(self, message):
        #we'll get to it after figuring out remote IP addressing
        pass

    @decorators.game_multicast_route
    def distribute_secret_word(self,message):
        outbound = Message({
            'message_type':'receive_new_secret_word',
            'secret_word':message.payload['secret_word'],
            })
        return outbound

    @decorators.game_multicast_route
    def distribute_guess(self, message):
        self.last_guess_id+=1
        self.active_guesses[self.last_guess_id] ={
            'guess_word':message.payload['guess_word'],
            'guess_clue':message.payload['guess_clue'],
            'blocks':[],
            'contacts':[]
        }
        outbound = Message({
            'message_type':'receive_new_guess',
            'guess_word':message.payload['guess_word'],
            'guess_clue':message.payload['guess_clue'],
            'guess_id':self.last_guess_id,
            })
        return outbound

    @decorators.game_multicast_route
    def distribute_contact(self, message):
        guess_id = message.payload['guess_id']
        self.active_guesses[guess_id]['contacts'].append(
            (
                message.payload['sender_id'],
                self.active_players[message.payload['sender_id']]['player_alias'],
                message.payload['contact_guess'],
                )
            )
        outbound = Message({
            'message_type':'receive_contact_notification',
            'guess_id':guess_id,
            'player_alias': self.active_players[message.payload['sender_id']]['player_alias']
            })
        return outbound

    def sender_id(self):
        return self.game_id


    @classmethod
    def set_up_controller(cls):
        if len(sys.argv) > 2:
            address, port, game_id = sys.argv[1:]
        else:
            address, port, game_id = "127.0.0.1" ,12018,17
        connection = NetworkIO((address, int(port)))

        game = Game(connection, **{'game_id':int(game_id)})
        print('g:booting up game %d' % game.game_id)
        print('g:address ', game.network_obj.address)
        return game

if __name__ == '__main__':
    game = Game.set_up_controller()
    while True:
        game.primary_loop()
