from message import Message
import decorators

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
