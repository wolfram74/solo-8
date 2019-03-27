import configparser
from player import Player
from message import Message
from network_io import NetworkIO
import select

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
    readers, _, _ = select.select([player.network_obj.socket], [],[],0)
    for reader in readers:
        player.network_obj.recieve()

    if player.network_obj.outbox:
        player.network_obj.transmit()

    if player.network_obj.inbox:
        print('got messages')
        msg = player.network_obj.inbox.pop(0)
        print(msg.payload)
        getattr(player, msg.payload['message_id'])(msg)
