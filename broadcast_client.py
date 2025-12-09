from socket import *
import threading
import sys
import pyaudio
import time


AUDIO_START = "AUDIO_START"
AUDIO_END = "AUDIO_END"

username = input("Enter your username: ")

def bg_thread(clientSocket):
    while True:
        try:
            data = clientSocket.recv(1024)
            if not data:
                print("Server closed the connection.")
                break
            
            try:
                text = data.decode().strip()
            except UnicodeDecodeError:
                continue

            if text != AUDIO_START:
                print(text)
            else:
                print("Receiving audio message ....")

                p = pyaudio.PyAudio()
                stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, output=True, frames_per_buffer=2048)

                while True:
                    data = clientSocket.recv(1024)
                    if not data:
                        break
                    
                    # Check if the audio is end
                    is_end = False
                    try:
                        maybe_text = data.decode().strip()
                        if maybe_text == AUDIO_END:
                            is_end = True
                    except UnicodeDecodeError:
                        # Decode fails. This is audio.
                        pass

                    if is_end:
                        print("Audio message finished.")
                        break
                    
                    stream.write(data)
                stream.stop_stream()
                stream.close()
                p.terminate()
        except Exception as e:
            print(f"Receive error: {e}")
            break
            
def main_thread(clientSocket):
    print("Type messages and press Enter to send.")
    print("To send a private message: @username message")
    print("To send an audio clip: enter !audio")
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
        if text.strip().lower() == "!audio":
            clientSocket.send(AUDIO_START.encode())

            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=2048)
            print("Recording will begin soon.")
            time.sleep(1)
            print("Recording in 3")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1")
            time.sleep(1)

            print("Recording for about 5 seconds...")

            duration_seconds = 5
            data_per_second = int (48000 / 2048)
            total_data = duration_seconds * data_per_second

            for _ in range(total_data):
                try:
                    data = stream.read(2048, exception_on_overflow=False)
                except OSError:
                    print("Audio input overflow, stopping recording early.")
                    break

                clientSocket.send(data)
            stream.close()
            p.terminate()

            clientSocket.send(AUDIO_END.encode())
            print("Audio sent!") 
        else:
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
