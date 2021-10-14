import socket

h = socket.gethostname()
ip=socket.gethostbyname(h)

s = socket.socket()
host = ip
port = 8080

s.bind((host, port))
s.listen(5)
c, address = s.accept()
print('Got connection from: ', address)
while True:
    c.send(raw_input('Server please type: '))
    print('From Client: ', c.recv(1024))
c.close()

