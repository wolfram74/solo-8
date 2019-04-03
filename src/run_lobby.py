import configparser
from lobby import Lobby
from network_io import NetworkIO
import select
import sys

mode = 'DEV'
if len(sys.argv)>1:
    mode = sys.argv[1]

config = configparser.ConfigParser()
config.read('config.ini')

connection = NetworkIO(
    (
        config[mode]['lobby_ip'],
        int(config[mode]['lobby_port'])
        )
    )
lobby = Lobby(connection, **config[mode])

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
            print(msg.payload)
            print('')
    if lobby.network_obj.persistent_messages:
        lobby.network_obj.retry_persistent_messages()
    if lobby.network_obj.outbox:
        print('sent messages')
        lobby.network_obj.transmit()
# lobby

