from lobby import Lobby
from player import Player
from message import Message
import subprocess
from time import time

def fake_new_game(player_obj):
    player.request_new_game()
    pass

def fake_submit_word(player_obj):
    player.network_obj.enque(Message({
        'message_type':'submit_secret_word',
        'secret_word':'quine'
        }))
    pass

if __name__ == '__main__':
    player = Player.set_up_controller()
    subprocess.Popen(
        ['python3','lobby.py']
        )
    player.request_player_id()
    start_time = time()
    benchmarks = [
    (1,fake_new_game),
    # (3,fake_submit_word),
    ]
    while True:
        player.primary_loop()
        if benchmarks and time()-start_time > benchmarks[0][0]:
            benchmarks[0][1](player)
            # getattr(player,benchmarks[0][1])()
            benchmarks.pop(0)


