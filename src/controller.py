import sys
import configparser
import select
from message import Message
import decorators
from network_io import NetworkIO

class Controller:
    def __init__(self, network_obj, **kwargs):
        self.network_obj = network_obj
        self.last_message_id = 0

    @decorators.route
    def send_ack(self, message):
        out_bound={
        'response_to':message.m_uid(),
        'destination':message.payload['origin'],
        'message_type':'ack'
        }
        return Message(payload=out_bound, persist=False)

    def ack(self, message):
        print('cool, terminal response to: ', message.payload['response_to'])

    def primary_loop(self):
        readers = self.get_readers()
        self.parse_readers(readers)
        self.process_inbox()
        self.query_persistent_messages()
        self.process_outbox()

    def get_readers(self):
        readers, _, _ = select.select([player.network_obj.socket], [],[],0)
        return readers

    def parse_readers(self, readers):
        for reader in readers:
            self.network_obj.receive()

    def process_inbox(self):
        if not self.network_obj.inbox:
            return
        msg = self.network_obj.inbox.pop(0)
        try:
            getattr(self, msg.payload['message_type'])(msg)
        except AttributeError:
            print('invalid method call caught on %d' % self.sender_id() )
        except:
            print('something weird happened on %d' %self.sender_id())
            try:
                print('pathological message')
                print(msg.payload)
            except:
                print('miscompiled message')

    def query_persistent_messages(self):
        if lobby.network_obj.persistent_messages:
            lobby.network_obj.retry_persistent_messages()

    def process_outbox(self):
        if lobby.network_obj.outbox:
            print('sent messages')
            lobby.network_obj.transmit()

