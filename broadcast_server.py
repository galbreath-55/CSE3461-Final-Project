from socket import *
import threading

user_map = {}  # username → socket

def client_handler(connectionSocket, connections, username):
    try:
        while True:
            data = connectionSocket.recv(1024)
            if not data:
                break
            text = data.decode().strip()

            # ====== Feature-2: private one-to-one ======
            if text.startswith("@"):
                # format: @target message
                if " " in text:
                    target, msg = text[1:].split(" ", 1)
                else:
                    target, msg = text[1:], ""

                target_sock = user_map.get(target)
                if target_sock:
                    try:
                        target_sock.send(f"[PRIVATE] {username}: {msg}".encode())
                    except Exception:
                        # target may have disconnected unexpectedly
                        connectionSocket.send("Failed to deliver private message.".encode())
                else:
                    connectionSocket.send("User not found or offline.".encode())
            # =========================================
            else:
                # Broadcast to all other clients
                for conn in list(connections):
                    if conn != connectionSocket:
                        try:
                            conn.send(f"{username}: {text}".encode())
                        except Exception:
                            # remove dead connections
                            try:
                                connections.remove(conn)
                            except ValueError:
                                pass
    except Exception as e:
        print(f"Error in client handler for {username}: {e}")
    finally:
        # Clean up on disconnect
        user_map.pop(username, None)
        try:
          connections.remove(connectionSocket)
        except ValueError:
          pass
        connectionSocket.close()
        print(f"[SERVER] {username} disconnected.")
    

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))

serverSocket.listen(5)
print("Server is running and listening...")
connections = []

while True:
    connectionSocket, addr = serverSocket.accept()
    
     # Ask client to identify with username
    connectionSocket.send("Enter your username: ".encode())
    username = connectionSocket.recv(1024).decode().strip()

    # Save mapping & connections
    user_map[username] = connectionSocket
    connections.append(connectionSocket)
    print(f"{username} connected!")

    # Start thread with username attached
    connectionThread = threading.Thread(
        target=client_handler,
        args=(connectionSocket,connections,username)
    )
    connectionThread.daemon = True
    connectionThread.start()