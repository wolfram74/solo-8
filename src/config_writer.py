import configparser
config = configparser.ConfigParser()
config['DEV'] = {
    'lobby_ip' : '127.0.0.1',
    'lobby_port' : '12001'
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)
