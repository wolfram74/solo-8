import unittest
import configparser
from message import Message
from game import Game

class TestGameRoutes(unittest.TestCase):
    def setUp(self):
        self.game = Game.set_up_controller()
        self.game.active_players ={
            1:{
            'player_alias':'p1',
            'player_address':('127.0.0.1',12001)
            },
            2:{
            'player_alias':'p2',
            'player_address':('127.0.0.1',12002)
            },
            3:{
            'player_alias':'p3',
            'player_address':('127.0.0.1',12003)
            },
        }
        self.message_in = Message({
            'message_id':17,
            'message_type':'generate_player_id',
            'sender_id':2,
            'origin':('127.0.0.1', 12003),
            'destination':('127.0.0.1', 120018),
            })

    def setUpGameWithWord(self):
        self.message_in.payload['message_type']='distribute_secret_word'
        self.message_in.payload['secret_word']='quine'
        self.game.distribute_secret_word(self.message_in)

    def setUpGameWithGuess(self):
        self.setUpGameWithWord()
        self.message_in.payload['message_type']='distribute_guess'
        self.message_in.payload['guess_word'] = 'query'
        self.message_in.payload['guess_clue'] = 'asking about something'
        self.game.distribute_guess(self.message_in)

    def setUpGameWithContacts(self):
        self.setUpGameWithGuess()
        self.message_in.payload['message_type']='distribute_contact'
        self.message_in.payload['contact_guess'] = 'query'
        self.message_in.payload['sender_id'] = 1
        self.message_in.payload['guess_id'] = self.game.last_guess_id
        self.game.distribute_contact(self.message_in)
        self.message_in.payload['message_type']='distribute_contact'
        self.message_in.payload['contact_guess'] = 'query'
        self.message_in.payload['sender_id'] = 2
        self.message_in.payload['guess_id'] = self.game.last_guess_id
        self.game.distribute_contact(self.message_in)
        self.message_in.payload['message_type']='distribute_contact'
        self.message_in.payload['contact_guess'] = 'qualia'
        self.message_in.payload['sender_id'] = 3
        self.message_in.payload['guess_id'] = self.game.last_guess_id
        self.game.distribute_contact(self.message_in)

    def tearDown(self):
        self.game.network_obj.socket.close()


    def testDistributeSecretWord(self):
        self.setUpGameWithWord()
        self.assertEqual(
            len(self.game.active_players),
            len(self.game.network_obj.outbox)
            )
        self.assertEqual(
            'receive_new_secret_word',
            self.game.network_obj.outbox[0].payload['message_type']
            )
        self.assertNotEqual(
            self.game.network_obj.outbox[0].payload['destination'],
            self.game.network_obj.outbox[1].payload['destination']
            )

    def testDistributeGuess(self):
        last_guess_id = self.game.last_guess_id
        self.setUpGameWithGuess()
        self.assertNotEqual(last_guess_id, self.game.last_guess_id)
        self.assertEqual(len(self.game.active_guesses), 1)
        self.assertEqual(
            2*len(self.game.active_players),
            len(self.game.network_obj.outbox)
            )

    def testDistributeContact(self):
        self.message_in.payload['message_type']='distribute_guess'
        self.message_in.payload['guess_word'] = 'query'
        self.message_in.payload['guess_clue'] = 'asking about something'
        self.game.distribute_guess(self.message_in)
        self.message_in.payload['message_type']='distribute_contact'
        self.message_in.payload['contact_guess'] = 'quest'
        self.message_in.payload['guess_id'] = self.game.last_guess_id
        self.game.distribute_contact(self.message_in)
        self.assertTrue(len(self.game.active_guesses[self.game.last_guess_id]['contacts'])==1)
        self.assertEqual(
            self.game.active_guesses[self.game.last_guess_id]['contacts'][0],
            (
                self.message_in.payload['sender_id'],
                self.game.active_players[self.message_in.payload['sender_id']]['player_alias'],
                self.message_in.payload['contact_guess']
                )
            )
        self.assertEqual(
            2*len(self.game.active_players),
            len(self.game.network_obj.outbox)
            )

    def testDistributeBlock(self):
        self.setUpGameWithContacts()
        self.message_in.payload['message_type']='distribute_block'
        self.message_in.payload['guess_block'] = 'query'
        self.message_in.payload['sender_id'] = 1
        self.message_in.payload['guess_id'] = self.game.last_guess_id
        self.game.distribute_block(self.message_in)

        self.assertEqual(
            len(self.game.network_obj.outbox[-1].payload['blocked_ids']), 2
            )
        self.assertEqual(
            self.game.network_obj.outbox[-1].payload['message_type'],
            'receive_block_resolution'
            )

    def testDistributeCall(self):
        self.setUpGameWithContacts()
        self.message_in.payload['message_type']='distribute_call'
        self.message_in.payload['sender_id'] = 1
        self.message_in.payload['guess_id'] = self.game.last_guess_id
        self.game.distribute_call(self.message_in)
        self.assertEqual(
            len(self.game.active_guesses), 0
            )
        self.assertEqual(
            self.game.network_obj.outbox[-1].payload['message_type'],
            'receive_call_resolution'
            )
        self.assertEqual(
            self.game.network_obj.outbox[-1].payload['call_success'],
            True
            )
