import socket

s = socket.socket()

s.connect(('localhost',9001))

s.send('election')
