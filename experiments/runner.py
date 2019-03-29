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
            ["python3", "sub_run.py", servers[loops]]
            )
        #note: if the parent process ends without stopping the child processes they can't be stopped with a simple meta-c
        #ps and kill can help
    # if loops >6:
    #     break
