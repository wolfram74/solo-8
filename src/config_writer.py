import configparser
config = configparser.ConfigParser()
config['DEV'] = {
    'lobby_ip' : '127.0.0.1',
    'lobby_port' : '12001',
    'player_ip' : '127.0.0.1',
    'player_port' : '12002',
    'game_id_step' : '17'
}

config['PROD'] = {
    'lobby_ip' : '54.214.53.85',
    # 'lobby_ip' : '172.31.24.81',
    'lobby_port' : '12001',
    'game_id_step' : '19'
}
with open('config.ini', 'w') as configfile:
    config.write(configfile)
