from socket import *
import threading

def client_handler(connectionSocket, connections):
    while connectionSocket.fileno() != -1:
        text = connectionSocket.recv(1024).decode()
        for c in connections:
            c.send(text.encode())

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))

serverSocket.listen(1)
connections = []

while 1:
    connectionSocket, addr = serverSocket.accept()
    connections.append(connectionSocket)
    connectionThread = threading.Thread(target=client_handler, args=(connectionSocket, connections))
    connectionThread.start()