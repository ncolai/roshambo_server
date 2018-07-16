#!/usr/bin/env python
import socket, sys

MAX_BYTES = 1024
HOST, PORT = "localhost", 9992
MOVES = ['rock', 'paper', 'scissors']
data = " ".join(sys.argv[1:])
client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_server.connect((HOST, PORT))
except:
    print("Couldn't connect to roshambo server...")

while True:
    move = raw_input('Ready to play: rock, paper or scissors?')
    client_server.send(move)
    received = client_server.recv(MAX_BYTES)
    if not received:
        continue
    elif received == 'ERROR':
        print("Not a valid move")
    else:
        status, computer_move = received.split(' ')
        print("The computer played {}".format(computer_move))
        if status != 'DRAW':
            print("You {}!".format(status))
            break
        else:
            print("You drew...")

client_server.close()


