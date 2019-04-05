import time
import sys
import socket
import select
special_arg = sys.argv[1]

loops = 0

connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
connection.bind(('0.0.0.0', 12018))
print('sub loop %d %s' % (loops, special_arg))
data= None
while True:
    readers, _, _ = select.select([connection], [],[],0)
    for reader in readers:
        data, address =connection.recvfrom(2**12)
    if data:
        print(data, address)

if __name__ == '__main__':
    print('howdy do')
