# CSE3461-Final-Project

This project is a simple multi-user chat system. Clients are able to connect to a server to send private messages, as well as broadcasts to all users. Users are able to initiate audio messages to other users connected using PyAudio, and Python's socket library.

## Requirements

Install the following dependencies:

- pip install pyaudio
- pip install keyboard

## Running the program

1. Start a server:

    - Run python broadcast_server.py
    - If the run is successful, the terminal will output "Server is running and listening..."
    - It may be needed to specify the local path to this file if python cannot locate it.

2. Join as clients:

    - Ensure that the "server_name" variable is correctly intialized to the IPv4 address of the server.
    - Run python broadcast_client.py
    - If the run is successful, the terminal will prompt the user to enter a username to complete the handshake.
    - Clients can enter messages to broadcast.
    - Prefix @user to privately message a user.
    - Enter !audio will begin transmitting audio to all users. Press q to end transmission.
    - Enter /quit or quit to end the connection.

## How audio transmission works

- When the user enters !audio, the client sends "AUDIO_START" to the server.
- The server forwards the same message to the receiving clients, and they begin receiving audio frames.
- The client sends raw audio to the server, which then sends them to all connection clients.
- Audio is sent and received in near real time.
- Audio is setup as a one way stream, and does not allow for overlapping audio.
