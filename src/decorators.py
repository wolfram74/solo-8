def route(route_to_be):
    #to be applied to classes with routes (lobby, player and game)
    #route methods take messages as inputs
    def routified(message):
        self.last_message_id +=1
        new_message = route_to_be(message)
        new_message['message_id'] = self.last_message_id
        new_message['sender_id'] = self.sender_id()
        new_message['origin'] = self.network_obj.address
        self.network_obj.enque(new_message)
