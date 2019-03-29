import configparser
from lobby import Lobby
from network_io import NetworkIO
import select
import sys

address, port, game_id = sys.argv[1:]

connection = NetworkIO((addres, int(port)))

game = Game(connection, {'game_id':int(game_id)})

while True:
    readers, _, _ = select.select([game.network_obj.socket], [],[],0)
    for reader in readers:
        game.network_obj.recieve()

    if game.network_obj.inbox:
        print('g:got messages')
        msg = game.network_obj.inbox.pop(0)
        # print(msg.payload)
        getattr(game, msg.payload['message_type'])(msg)
    if game.network_obj.outbox:
        print('g:sent messages')
        game.network_obj.transmit()

