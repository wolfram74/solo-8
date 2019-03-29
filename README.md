# solo-8
ideas for code improvement:
many message senders have common features, such as incrementing the message id counter and enqueing a produced message, maybe a decorator that reduces code reuse?

echo '{"message_id": 3, "sender_id": 3, "player_id": 3, "player_alias": "farts", "destination": ["127.0.0.1", 12052], "origin": ["127.0.0.1", 12002], "message_type": "add_new_player"}' > /dev/udp/127.0.0.1/12018

echo '{"message_id": 1, "message_type": "generate_player_id", "destination": ["45.55.178.89", 12001], "player_alias": "farts"}' > /dev/udp/45.55.178.89:12001

echo "foo" | nc -w1 -u 45.55.178.89 12001
nmap -p 11000-12010 45.55.178.89
nmap -sUV 45.55.178.89 -p 11999-12010
