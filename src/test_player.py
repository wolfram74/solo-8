import unittest
import configparser
from message import Message
from player import Player

class TestInterfaceTriggeredRoutes(unittest.TestCase):
    def setUp(self):
        self.player = Player.set_up_controller()
        self.dumby_message = Message({
            'message_id':1,
            'message_type':'generate_player_id',
            'sender_id':2,
            'origin':('127.0.0.1', 12003),
            'destination':('127.0.0.1', 12001),
            })

    def tearDown(self):
        self.player.network_obj.socket.close()

    def testRequestPlayerID(self):
        self.player.request_player_id()
        self.assertTrue(
            len(self.player.network_obj.outbox)==1)
        self.assertEqual(
            self.player.network_obj.outbox[0].payload['message_type'],
            'generate_player_id'
            )



