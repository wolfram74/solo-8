import time
import sys

special_arg = sys.argv[1]

loops = 0

while True:
    print('sub loop %d %s' % (loops, special_arg))
    time.sleep(2)
    loops+=1
