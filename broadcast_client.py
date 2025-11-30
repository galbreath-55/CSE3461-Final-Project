from socket import *
import threading
from time import sleep

def bg_thread(clientSocket):
    while 1:
        text = clientSocket.recv(1024).decode()
        print("RECEIVED FROM SERVER: " + text)

def main_thread(clientSocket):
    while 1:
        sleep(1)
        print("Please enter a message to send to the server: ")
        text = input()
        clientSocket.send(text.encode())

serverName = "127.0.0.1"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

print("This device's local address is: ", clientSocket.getsockname()[0], ", and the port # is: ", clientSocket.getsockname()[1])

backgroundThread = threading.Thread(target=bg_thread, args=(clientSocket,))
mainThread = threading.Thread(target=main_thread, args=(clientSocket,))
backgroundThread.start()
mainThread.start()

backgroundThread.join()
mainThread.join()