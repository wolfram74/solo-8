def route(route_to_be):
    #to be applied to classes with routes (lobby, player and game)
    #route methods take messages as inputs
    def routified(self, message=None):
        # print('dec:', message, message.payload)
        self.last_message_id +=1
        if message:
            new_message = route_to_be(self, message)
        else:
            new_message = route_to_be(self)
        new_message.payload['message_id'] = self.last_message_id
        new_message.payload['sender_id'] = self.sender_id()
        new_message.payload['origin'] = self.network_obj.address
        self.network_obj.enque(new_message)
        return message
    return routified
