#https://docs.python.org/3/library/subprocess.html
import subprocess
import time
loops = 0

servers = ['','farts', 'glamdring', 'flebulon']
command_template = 'python3 sub_run.py %s'

while True:
    print('loop %d' %loops)
    time.sleep(2)
    loops+=1
    if loops < 4 and loops > 0:
        subprocess.Popen(
            command_template % servers[loops]  , shell=True
            )
