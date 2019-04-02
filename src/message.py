import json

def encoding(subject):
    return json.dumps(subject).encode()

def decoding(message_string):
    return json.loads(message_string.decode())

class Message():
    def __init__(self, payload, persist=True):
        self.payload = payload
        self.persistent=persist

    def encode(self):
        return encoding(self.payload)

    def destination(self):
        return tuple(self.payload['destination'])

    def m_uid(self):
        return (
            self.payload['message_type'],
            self.payload['sender_id'],
            self.payload['message_id']
            )

    @classmethod
    def fromByteString(cls, byte_string):
        unpacked_dict = decoding(byte_string)
        return Message(unpacked_dict)
