import json

def encoding(subject):
    return json.dumps(subject).encode()

def decoding(message_string):
    return json.loads(message_string.decode())

class Message():
    def __init__(self, payload):
        self.payload = payload

    def encode(self):
        return encoding(self.payload)

    def destination(self):
        return tuple(self.payload['destination'])

    @classmethod
    def fromByteString(cls, byte_string):
        unpacked_dict = decoding(byte_string)
        return Message(unpacked_dict)
