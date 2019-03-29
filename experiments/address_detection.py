import socket
hostname = socket.gethostname()
print("Your Computer Name is:" + hostname)
IPAddr = socket.gethostbyname(hostname)
print("Your Computer IP Address is:" + IPAddr)
