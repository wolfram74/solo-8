import unittest
from message import Message

class TestMessageReversability(unittest.TestCase):
    def testReversability(self):
        message = Message({
            'message_id':'generate_player_id',
            'alias':'fart',
            'destination':['127.0.9.1', 84]
            })
        newMess = Message.fromByteString(message.encode())
        self.assertEqual(message.payload, newMess.payload)

if __name__ == "__main__":
    unittest.main()
