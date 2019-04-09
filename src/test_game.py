import unittest
import configparser
from message import Message
from game import Game

class TestGameRoutes(unittest.TestCase):
    def setUp(self):
        self.game = Game.set_up_controller()
        self.game.active_players ={
            1:{
            'player_alias':'p1',
            'player_address':('127.0.0.1',12001)
            },
            2:{
            'player_alias':'p2',
            'player_address':('127.0.0.1',12002)
            },
            3:{
            'player_alias':'p3',
            'player_address':('127.0.0.1',12003)
            },
        }
        self.message_in = Message({
            'message_id':17,
            'message_type':'generate_player_id',
            'sender_id':2,
            'origin':('127.0.0.1', 12003),
            'destination':('127.0.0.1', 12002),
            })

    def tearDown(self):
        self.game.network_obj.socket.close()

    def testDistributeSecretWord(self):
        self.message_in.payload['message_type']='distribute_secret_word'
        self.message_in.payload['secret_word']='quine'
        self.game.distribute_secret_word(self.message_in)
        self.assertEqual(
            len(self.game.active_players),
            len(self.game.network_obj.outbox)
            )
        self.assertEqual(
            'receive_new_secret_word',
            self.game.network_obj.outbox[0].payload['message_type']
            )
        self.assertNotEqual(
            self.game.network_obj.outbox[0].payload['destination'],
            self.game.network_obj.outbox[1].payload['destination']
            )