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
