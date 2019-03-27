import configparser
from lobby import Lobby
from network_io import NetworkIO

config = configparser.ConfigParser()
config.read('config.ini')

connection = NetworkIO(
    (
        config['DEV']['lobby_ip'],
        int(config['DEV']['lobby_port'])
        )
    )
lobby = Lobby(connection)

while True:
    lobby.network_obj.recieve()
    if lobby.network_obj.inbox:
        print('got messages')
        msg = lobby.network_obj.inbox.pop(0)
        print(msg.payload)
        getattr(lobby, msg.payload['message_id'])(msg)

# lobby

