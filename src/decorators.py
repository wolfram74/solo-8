import copy
def route(route_to_be):
    #to be applied to classes with routes (lobby, player and game)
    #route methods take messages as inputs and have message outputs
    #methods that end by calling send_ack, while can be invoked by new messages, should not be designated as routes
    def routified(self, message=None):
        # print('dec:', message, message.payload)
        self.last_message_id +=1
        if message:
            new_message = route_to_be(self, message)
            new_message.payload['response_to'] = message.m_uid()
        else:
            new_message = route_to_be(self)
        new_message.payload['message_id'] = self.last_message_id
        new_message.payload['sender_id'] = self.sender_id()
        new_message.payload['origin'] = self.network_obj.address
        self.network_obj.enque(new_message)
        return message
    return routified

def game_multicast_route(route_to_be):
    def routified(self,message):
        new_message = route_to_be(self, message)
        new_message.payload['sender_id'] = self.sender_id()
        new_message.payload['origin'] = self.network_obj.address
        new_message.payload['response_to'] = message.m_uid()
        for player_id in self.active_players.keys():
            player = self.active_players[player_id]
            play_message = copy.deepcopy(new_message)
            self.last_message_id +=1
            play_message.payload['message_id'] = self.last_message_id
            play_message.payload['destination']=player['player_address']
            self.network_obj.enque(play_message)
        return message
    return routified

#possible TODO: make new "terminus_route" decorator
