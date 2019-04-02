import configparser
from player import Player
from message import Message
from network_io import NetworkIO
import select
from time import time
import sys

mode = 'DEV'
if len(sys.argv)>1:
    mode = sys.argv[1]


config = configparser.ConfigParser()
config.read('config.ini')

# connection = NetworkIO(
#     (
#         config['DEV']['player_ip'],
#         int(config['DEV']['player_port'])
#         )
#     )
connection = NetworkIO()
lobby_address =     (
    config[mode]['lobby_ip'],
    int(config[mode]['lobby_port'])
    )

player = Player(connection, lobby_address)
player.request_player_id()
start_time = time()
benchmarks = [(1,'request_new_game')]


while True:
    readers, _, _ = select.select([player.network_obj.socket], [],[],0)
    for reader in readers:
        player.network_obj.receive()


    if player.network_obj.inbox:
        print('got messages')
        msg = player.network_obj.inbox.pop(0)
        print(msg.payload)
        getattr(player, msg.payload['message_type'])(msg)

    if player.network_obj.persistent_messages:
        player.network_obj.retry_persistent_messages()

    if player.network_obj.outbox:
        player.network_obj.transmit()

    if benchmarks and time()-start_time > benchmarks[0][0]:
        getattr(player,benchmarks[0][1])()
        benchmarks.pop(0)
