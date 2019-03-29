import configparser
from lobby import Lobby
from network_io import NetworkIO
import select

config = configparser.ConfigParser()
config.read('config.ini')

connection = NetworkIO(
    (
        config['DEV']['lobby_ip'],
        int(config['DEV']['lobby_port'])
        )
    )
lobby = Lobby(connection, **config['DEV'])

print('l: ', lobby.network_obj.socket)
while True:
    readers, _, _ = select.select([lobby.network_obj.socket], [],[],0)
    for reader in readers:
        lobby.network_obj.receive()

    if lobby.network_obj.inbox:
        print('got messages')
        try:
            msg = lobby.network_obj.inbox.pop(0)
            getattr(lobby, msg.payload['message_type'])(msg)
        except AttributeError:
            print('l: invalid method call caught')
        except:
            print('l: something weird happened on receipt')
    if lobby.network_obj.outbox:
        print('sent messages')
        lobby.network_obj.transmit()
# lobby

