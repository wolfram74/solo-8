import socket
from message import Message
from time import time

class NetworkIO():
    def __init__(self, address=None, retry_time = 1.):
        #address is ('ip',port_int)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = address
        if address:
            self.socket.bind(('0.0.0.0' ,address[1]))
        self.inbox = []
        self.outbox = []
        self.persistent_messages = {}
        self.seen_messages = set()
        self.retry_time = retry_time

    def transmit(self):
        next_message = self.outbox.pop(0)
        # print('io:sending id:%d, dest: ' % next_message.payload['message_id'], next_message.destination())
        # print('io:byte_length %d ' % len(next_message.encode()))
        # print('io:byte_str %s ' % next_message.encode())
        # print(next_message)
        # print(next_message.payload)
        m_uid = next_message.m_uid()
        next_message.set_last_sent(time())
        if next_message.persistent:
            self.persistent_messages[m_uid] = next_message

        self.socket.sendto(
            next_message.encode(),
            next_message.destination()
            )
        # print('io: finished send')

    def receive(self):
        # print('io:receiveing')
        data, address =self.socket.recvfrom(2**12)
        print('io: address field?', address)
        new_message = Message.fromByteString(data)
        if 'origin' not in new_message.payload.keys():
            new_message.payload['origin'] = address
        if new_message.payload['origin'] == None:
            new_message.payload['origin'] = address

        self.seen_messages.add(new_message.m_uid())
        if 'response_to' in new_message.payload.keys():
            del self.persistent_messages[tuple(new_message.payload['response_to'])]
        self.inbox.append(
            new_message
            )

    def enque(self,message):
        self.outbox.append(message)


    def retry_persistent_messages(self):
        now = time()
        for m_uid in self.persistent_messages.keys():
            delta = now-self.persistent_messages[m_uid].last_sent
            if delta > self.retry_time:
                print(delta, self.persistent_messages[m_uid].payload)
                self.enque(self.persistent_messages[m_uid])
