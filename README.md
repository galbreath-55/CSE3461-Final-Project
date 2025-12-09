# CSE3461-Final-Project

This project is a simple multi-user chat system. Clients are able to connect to a server to send private messages, as well as broadcasts to all users. Users are able to initiate audio messages to other users connected using PyAudio, and Python's socket library.

## Requirements

Install the following dependencies (preferably in a virtual environment):

- pip3 install pyaudio
On macOS, you may need to install PortAudio first:

- brew install portaudio
- pip3 install pyaudio


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
    - Enter `!audio` to begin transmitting an audio clip to all users. The client records for about 5 seconds and then automatically ends the transmission.
    - Enter /quit or quit to end the connection.

## How audio transmission works

- When the user enters `!audio`, the client sends the control message `"AUDIO_START"` to the server.
- The server forwards `"AUDIO_START"` to all other connected clients. Upon receiving this, they switch into audio-receiving mode and start reading raw audio frames from the socket.
- The sending client records a short audio clip (about 5 seconds) using PyAudio and streams the raw audio frames to the server.
- The server rebroadcasts these audio frames to all other clients in (near) real time.
- After finishing the recording, the sender transmits an `"AUDIO_END"` control message. The server forwards this to the receivers, which causes them to stop audio playback and return to normal text mode.
- Audio is currently one-way: only one user speaks at a time, and overlapping audio is not supported.
