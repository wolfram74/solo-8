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
player.request_player_id()

while True:
    if player.network_obj.outbox:
        player.network_obj.transmit()
