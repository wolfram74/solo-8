import socket
from message import Message

class NetworkIO():
    def __init__(self, address):
        #address is ('ip',port_int)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = address
        self.socket.bind(address)
        self.inbox = []
        self.outbox = []

    def transmit(self):
        next_message = self.outbox.pop(0)
        print('io:sending id:%d, dest: ' % next_message.payload['message_id'], next_message.destination())
        self.socket.sendto(
            next_message.encode(),
            next_message.destination()
            )
        print('io: finished send')
    def recieve(self):
        print('io:recieveing')
        data, address =self.socket.recvfrom(2**12)
        print('io: address field?', address)
        self.inbox.append(
            Message.fromByteString(data)
            )

    def enque(self,message):
        self.outbox.append(message)
