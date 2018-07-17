#!/usr/bin/env python
import socket, sys, time

MAX_BYTES = 1024
MAX_TIME = 0.1
HOST, PORT = "localhost", 9992
MOVES = ['rock', 'paper', 'scissors']
data = " ".join(sys.argv[1:])
client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
start_time = time.clock()
has_connection = False
print("Connecting to server...")
while True:
    try:
        client_server.connect((HOST, PORT))
        has_connection = True
        break
    except:
        has_connection = False
        if time.clock() - start_time > MAX_TIME:
            print("Timed out after waiting {} seconds".format(MAX_TIME))
            break

while has_connection:
    move = raw_input('Ready to play: rock, paper or scissors?')
    while move not in MOVES: #error checking so we send a correct move to the server
        move = raw_input('Invalid move choice, try again:')
    client_server.send(move)
    print("Waiting for opponent...")
    received = client_server.recv(MAX_BYTES)
    if not received:
        continue
    elif received == 'ERROR':
        print("Not a valid move")
    else:
        status, computer_move = received.split(' ')
        print("Your opponent played {}".format(computer_move))
        if status != 'DRAW':
            print("You {}!".format(status))
            break
        else:
            print("You drew...")

client_server.close()


