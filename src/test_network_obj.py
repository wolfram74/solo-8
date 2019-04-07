import unittest
from network_io import NetworkIO
from message import Message

class MockSock():
    def __init__(self):
        self.queue = []
    def recv(self, bits):
        return self.queue.pop(0)

    def sendto(self, bits, address):
        self.queue.append((bits, address))

class TestNetworkObjBehavior(unittest.TestCase):
    def setUp(self):
        self.network_obj = NetworkIO()
        self.network_obj.socket.close()
        self.network_obj.socket = MockSock()
        self.dumby_message = Message({
            'message_id':1
            'sender_id':1
            'origin':('127.0.0.1', 12003)
            })

    def testTransmit(self):
        pass
    def testRecieving(self):
        pass
    def testReceiveDupe(self):
        pass
    def testEndPersistence(self):
        pass
