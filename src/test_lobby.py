import unittest
import configparser
from network_io import NetworkIO
from message import Message
from lobby import Lobby

config = configparser.ConfigParser()
config.read('./src/config.ini')

connection = NetworkIO(
    (
    config['DEV']['lobby_ip'],
    int(config['DEV']['lobby_port'])
    )
)


class TestLobbyIdAssignment(unittest.TestCase):
    def testAssignment(self):
        lobby = Lobby(connection, **config['DEV'])
        for i in range(5):
            msg = Message({
                'player_alias':'fart%d'%i,
                'origin':['127.0.0.1',137],
                'destination':lobby.network_obj.address
                })
            lobby.generate_player_id(msg)
        self.assertEqual(len(lobby.network_obj.outbox),5)
        self.assertEqual(len(lobby.active_players.keys()),5)

    def testCollisionAvoidance(self):
        lobby = Lobby(connection, **config['DEV'])
        for i in range(50):
            msg = Message({
                'player_alias':'fart%d'%i,
                'origin':['127.0.0.1',137],
                'destination':lobby.network_obj.address
                })
            lobby.generate_player_id(msg)
        for j in range(3):
            lobby.generate_game_id()
        no_collision = True
        for game_id in lobby.active_games.keys():
            no_collision = no_collision and (game_id not in lobby.active_players)
        self.assertTrue(no_collision)
