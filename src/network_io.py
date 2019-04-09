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
        print(next_message.payload)
        m_uid = next_message.m_uid()
        next_message.set_last_sent(time())
        if next_message.persistent:
            self.persistent_messages[m_uid] = next_message

        self.socket.sendto(
            next_message.encode(),
            next_message.destination()
            )

    def receive(self):
        # print('io:receiveing')
        data, address =self.socket.recvfrom(2**12)
        # print('io: address field?', address)
        new_message = Message.fromByteString(data)
        if 'origin' not in new_message.payload.keys():
            new_message.payload['origin'] = address
        if new_message.payload['origin'] == None:
            new_message.payload['origin'] = address

        is_repeat = self.check_for_repeat(new_message)
        if is_repeat:
            self.deter_repeat_messages(new_message)
            return

        self.seen_messages.add(new_message.m_uid())
        if 'response_to' in new_message.payload.keys():
            # print('response', new_message.payload)
            if tuple(new_message.payload['response_to']) in self.persistent_messages:
                del self.persistent_messages[
                    tuple(new_message.payload['response_to'])
                    ]
        self.inbox.append(
            new_message
            )

    def enque(self,message):
        self.outbox.append(message)

    def check_for_repeat(self, message):
        if message.payload['sender_id']==0:
            return False
        if message.m_uid() in self.seen_messages:
            return True
        return False

    def retry_persistent_messages(self):
        now = time()
        for m_uid in self.persistent_messages.keys():
            delta = now-self.persistent_messages[m_uid].last_sent
            if delta > self.retry_time:
                print(delta, self.persistent_messages[m_uid].payload)
                self.enque(self.persistent_messages[m_uid])


    def deter_repeat_messages(self,message):
        print('io:dupe message')
        stop_message = Message({
            'response_to': message.m_uid(),
            'message_type': 'ack',
            'sender_id': 0,
            'message_id': 0,
            'origin':self.address,
            'destination':message.payload['origin'],
            })
        self.enque(stop_message)

