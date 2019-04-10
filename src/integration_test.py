from lobby import Lobby
from player import Player
from message import Message
import subprocess
from time import time

def fake_new_game(player_obj):
    player.request_new_game()
    pass

def fake_submit_word(player_obj):
    player.network_obj.inbox.append(Message({
        'message_type':'submit_secret_word',
        'sender_id':'t',
        'secret_word':'quine'
        }))
    pass

def fake_submit_guess(player_obj):
    player.network_obj.inbox.append(Message({
        'message_type':'submit_guess',
        'sender_id':'t',
        'guess_word':'query',
        'guess_clue':'asking a question'
        }))

def fake_submit_contact(player_obj):
    player.network_obj.inbox.append(Message({
        'message_type':'submit_contact',
        'sender_id':'t',
        'guess_id':1,
        'contact_guess':'question',
        }))


if __name__ == '__main__':
    player = Player.set_up_controller()
    subprocess.Popen(
        ['python3','lobby.py']
        )
    player.request_player_id()
    start_time = time()
    benchmarks = [
    (2,fake_new_game),
    (4,fake_submit_word),
    (6,fake_submit_guess),
    (8,fake_submit_contact),
    ]
    while True:
        player.primary_loop()
        if benchmarks and time()-start_time > benchmarks[0][0]:
            benchmarks[0][1](player)
            # getattr(player,benchmarks[0][1])()
            benchmarks.pop(0)


