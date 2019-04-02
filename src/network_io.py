import socket
from message import Message

class NetworkIO():
    def __init__(self, address=None):
        #address is ('ip',port_int)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = address
        if address:
            self.socket.bind(('0.0.0.0' ,address[1]))
        self.inbox = []
        self.outbox = []

    def transmit(self):
        next_message = self.outbox.pop(0)
        print('io:sending id:%d, dest: ' % next_message.payload['message_id'], next_message.destination())
        print('io:byte_length %d ' % len(next_message.encode()))
        print('io:byte_str %s ' % next_message.encode())
        self.socket.sendto(
            next_message.encode(),
            next_message.destination()
            )
        print('io: finished send')
    def receive(self):
        print('io:receiveing')
        data, address =self.socket.recvfrom(2**12)
        print('io: address field?', address)
        new_message = Message.fromByteString(data)
        if 'origin' not in new_message.payload.keys():
            new_message.payload['origin'] = address
        self.inbox.append(
            new_message
            )

    def enque(self,message):
        self.outbox.append(message)
