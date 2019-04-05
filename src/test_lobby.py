import unittest
import configparser
from network_io import NetworkIO
from message import Message
from lobby import Lobby



class TestLobbyIdAssignment(unittest.TestCase):
    def setUp(self):
        self.lobby = Lobby.set_up_controller()

    def tearDown(self):
        self.lobby.network_obj.socket.close()

    def testAssignment(self):
        for i in range(5):
            msg = Message({
                'player_alias':'fart%d'%i,
                'origin':['127.0.0.1',0],
                'sender_id':0,
                'message_id':1,
                'message_type':'generate_player_id',
                'destination':self.lobby.network_obj.address
                })
            self.lobby.generate_player_id(msg)
        self.assertEqual(len(self.lobby.network_obj.outbox),5)
        self.assertEqual(len(self.lobby.active_players.keys()),5)

    def testCollisionAvoidance(self):

        for i in range(50):
            msg = Message({
                'player_alias':'fart%d'%i,
                'origin':['127.0.0.1',0],
                'sender_id':0,
                'message_id':1,
                'message_type':'generate_player_id',
                'destination':self.lobby.network_obj.address
                })
            self.lobby.generate_player_id(msg)
        for j in range(3):
            self.lobby.generate_game_id()
        no_collision = True
        for game_id in self.lobby.active_games.keys():
            no_collision = no_collision and (game_id not in self.lobby.active_players)
        self.assertTrue(no_collision)
