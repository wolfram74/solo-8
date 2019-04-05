from lobby import Lobby
from player import Player
import subprocess
from time import time

if __name__ == '__main__':
    player = Player.set_up_controller()
    subprocess.Popen(
        ['python3','lobby.py']
        )
    player.request_player_id()
    start_time = time()
    benchmarks = [(1,'request_new_game')]
    while True:
        player.primary_loop()
        if benchmarks and time()-start_time > benchmarks[0][0]:
            getattr(player,benchmarks[0][1])()
            benchmarks.pop(0)

