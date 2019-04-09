import unittest
import configparser
from message import Message
from player import Player

class TestPlayerRoutes(unittest.TestCase):
    def setUp(self):
        self.player = Player.set_up_controller()
        self.message_in = Message({
            'message_id':1,
            'message_type':'generate_player_id',
            'sender_id':2,
            'origin':('127.0.0.1', 12003),
            'destination':('127.0.0.1', 12001),
            })

    def tearDown(self):
        self.player.network_obj.socket.close()

    def testRequestPlayerID(self):
        self.player.request_player_id()
        self.assertTrue(
            len(self.player.network_obj.outbox)==1)
        self.assertEqual(
            self.player.network_obj.outbox[0].payload['message_type'],
            'generate_player_id'
            )

    def testSubmitSecretWord(self):
        self.message_in.payload['message_type']='submit_secret_word'
        self.message_in.payload['secret_word']='quine'
        self.player.submit_secret_word(self.message_in)
        self.assertTrue(
            len(self.player.network_obj.outbox)==1)
        self.assertEqual(
            self.player.network_obj.outbox[0].payload['message_type'],
            'distribute_secret_word'
            )

    def testReceiveNewSecretWord(self):
        self.message_in.payload['message_type']='receive_new_secret_word'
        self.message_in.payload['secret_word']='quine'
        self.player.receive_new_secret_word(self.message_in)
        self.assertTrue(
            len(self.player.network_obj.outbox)==1)
        self.assertEqual(
            self.player.network_obj.outbox[0].payload['message_type'],
            'ack'
            )
        self.assertEqual(self.player.secret_word, 'quine')
        self.assertEqual(self.player.visible_word(), 'q')
        self.assertEqual(self.player.visible_letters, 1)

    def testSubmitGuess(self):
        self.message_in.payload['message_type'] = 'submit_guess'
        self.message_in.payload['guess_word'] = 'query'
        self.message_in.payload['guess_clue'] = 'asking about something'
        self.message_in.payload['sender_id'] = 't'
        self.player.submit_guess(self.message_in)
        self.assertTrue(len(self.player.network_obj.outbox)==1)
        self.assertEqual(
            self.player.network_obj.outbox[0].payload['message_type'],
            'distribute_guess'
            )


    def testReceiveNewGuess(self):
        self.message_in.payload['message_type'] = 'receive_new_guess'
        self.message_in.payload['guess_word'] = 'query'
        self.message_in.payload['guess_clue'] = 'asking about something'
        self.message_in.payload['guess_id'] = 7
        self.message_in.payload['sender_id'] = 3
        self.assertTrue(len(self.player.active_clues)==0)
        self.player.receive_new_guess(self.message_in)
        self.assertTrue(len(self.player.active_clues)==1)
        self.assertTrue(len(self.player.network_obj.outbox)==1)
        self.assertEqual(
            self.player.network_obj.outbox[0].payload['message_type'],
            'ack'
            )

    @unittest.skip('deferred')
    def testSubmitContact(self):
        pass

    @unittest.skip('deferred')
    def testReceiveContactNotification(self):
        pass

    @unittest.skip('deferred')
    def testSubmitBlock(self):
        pass

    @unittest.skip('deferred')
    def testReceiveBlockResolution(self):
        pass

    @unittest.skip('deferred')
    def testSubmitCall(self):
        pass

    @unittest.skip('deferred')
    def testReceiveCallResolution(self):
        pass


