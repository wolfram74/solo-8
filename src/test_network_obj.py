import unittest
import copy
from network_io import NetworkIO
from message import Message

class MockSock():
    def __init__(self):
        self.queue = []
    def recvfrom(self, bits):
        result = self.queue.pop(0)
        return result[0], result[1]

    def sendto(self, bits, address):
        self.queue.append((bits, address))

class TestNetworkObjBehavior(unittest.TestCase):
    def setUp(self):
        self.network_obj = NetworkIO()
        self.network_obj.socket.close()
        self.network_obj.socket = MockSock()
        self.dumby_message = Message({
            'message_id':1,
            'message_type':'generate_player_id',
            'sender_id':0,
            'origin':('127.0.0.1', 12003),
            'destination':('127.0.0.1', 12001),
            })

    def testTransmit(self):
        self.network_obj.enque(self.dumby_message)
        self.network_obj.transmit()
        self.assertEqual(len(self.network_obj.outbox), 0)

    def testRecieving(self):
        self.network_obj.socket.queue.append((
            self.dumby_message.encode(),
            self.dumby_message.payload['origin']
                ))
        self.network_obj.receive()
        self.assertEqual(len(self.network_obj.inbox), 1)
        self.assertEqual(type(self.network_obj.inbox[0]), Message)

    def testReceiveDupe(self):
        self.dumby_message.payload['sender_id']=1
        self.dumby_message.payload['message_type']='start_new_game'
        self.network_obj.socket.queue.append((
            self.dumby_message.encode(),
            self.dumby_message.payload['origin']
                ))
        self.network_obj.socket.queue.append((
            self.dumby_message.encode(),
            self.dumby_message.payload['origin']
                ))
        self.network_obj.receive()
        self.network_obj.receive()
        self.assertEqual(len(self.network_obj.inbox), 1)
        self.assertEqual(len(self.network_obj.outbox), 1)
        self.assertEqual(len(self.network_obj.outbox), 1)
        self.assertEqual(len(self.network_obj.seen_messages), 1)

    def testEndPersistence(self):
        self.network_obj.enque(self.dumby_message)
        self.network_obj.transmit()
        self.network_obj.receive()
        self.assertEqual(len(self.network_obj.persistent_messages),1)
        stop_message = copy.copy(self.dumby_message)
        stop_message.payload['response_to']=self.dumby_message.m_uid()
        stop_message.payload['message_id']=4
        stop_message.payload['sender_id']=121
        stop_message.payload['message_type']='ack'
        stop_message.persistent= False
        self.network_obj.enque(stop_message)
        self.network_obj.transmit()
        self.network_obj.receive()
        self.assertEqual(len(self.network_obj.persistent_messages),0)

