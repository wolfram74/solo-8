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

# lobby

