import socket

connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

connection.sendto('farts'.encode(), ('127.0.0.1', 12018))
