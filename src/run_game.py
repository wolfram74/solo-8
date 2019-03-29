import configparser
from game import Game
from network_io import NetworkIO
import select
import sys

address, port, game_id = sys.argv[1:]

connection = NetworkIO((address, int(port)))

game = Game(connection, **{'game_id':int(game_id)})
print('g:booting up game %d' % game.game_id)
print('g:address ', game.network_obj.address)
print('g:', game.network_obj.socket)
while True:
    readers, _, _ = select.select([game.network_obj.socket], [],[],0)
    for reader in readers:
        game.network_obj.receive()

    if game.network_obj.inbox:
        print('g:got messages')
        msg = game.network_obj.inbox.pop(0)
        # print(msg.payload)
        getattr(game, msg.payload['message_type'])(msg)
    if game.network_obj.outbox:
        print('g:sent messages')
        game.network_obj.transmit()

