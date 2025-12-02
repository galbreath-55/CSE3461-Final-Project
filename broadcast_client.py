from socket import *
import threading
import sys

username = input("Enter your username: ")

def bg_thread(clientSocket):
    while True:
        try:
            data = clientSocket.recv(1024)
            if not data:
                print("Server closed the connection.")
                break
            text = data.decode()
            print(text)
        except Exception as e:
            print(f"Receive error: {e}")
            break

def main_thread(clientSocket):
    print("Type messages and press Enter to send.")
    print("To send a private message: @username message")
    print("To quit: /quit")
    while True:
        try:
            text = input()
        except EOFError:
            break

        if not text:
            continue

        if text.strip().lower() in ("/quit", "quit", "/exit"):
            try:
                clientSocket.close()
            except Exception:
                pass
            break

        try:
            clientSocket.send(text.encode())
        except Exception as e:
            print(f"Send failed: {e}")
            break

serverName = "127.0.0.1"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Receive “Enter your username:” prompt from server and send username mapping
try:
    clientSocket.recv(1024)
    clientSocket.send(username.encode())
except Exception as e:
    print(f"Failed to complete handshake with server: {e}")
    sys.exit(1)

print("Connected as:", username)
print("Local address:", clientSocket.getsockname())

backgroundThread = threading.Thread(target=bg_thread, args=(clientSocket,))
backgroundThread.daemon = True
mainThread = threading.Thread(target=main_thread, args=(clientSocket,))
backgroundThread.start()
mainThread.start()

mainThread.join()
# when mainThread exits, ensure socket closed so bg_thread breaks
try:
    clientSocket.close()
except Exception:
    pass
backgroundThread.join()