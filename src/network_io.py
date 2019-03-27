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
        print('sending')
        self.socket.sendto(
            next_message.encode(),
            next_message.destination()
            )

    def recieve(self):
        print('recieveing')
        data, address =self.socket.recvfrom(2**12)
        self.inbox.append(
            Message.fromByteString(data)
            )

    def enque(self,message):
        self.outbox.append(message)
