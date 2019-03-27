import configparser
from player import Player
from message import Message
from network_io import NetworkIO

config = configparser.ConfigParser()
config.read('config.ini')

connection = NetworkIO(
    (
        config['DEV']['player_ip'],
        int(config['DEV']['player_port'])
        )
    )
lobby_address =     (
    config['DEV']['lobby_ip'],
    int(config['DEV']['lobby_port'])
    )

player = Player(connection, lobby_address)
test_message = Message(
    {'message_id':0, 'player_alias':'farts', 'destination':lobby_address})
player.network_obj.outbox.append(test_message)
player.network_obj.transmit()
