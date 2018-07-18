#!/usr/bin/env python
import socket, sys, time
#custom libraries
import utils
from utils import HandshakeCode

MAX_TIME = 0.1
HOST, PORT = "localhost", 9990
MOVES = ['rock', 'paper', 'scissors']
data = " ".join(sys.argv[1:])
client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
start_time = time.clock()
has_connection = False
version = 1
print("Connecting to server...")
while True: 
    try:
        client_server.connect((HOST, PORT))
        #send a handshake
        utils.send_packet(client_server, version)
        handshake_return = utils.receive_packet(client_server)
        print(handshake_return)
        if handshake_return != str(HandshakeCode.HANDSHAKE_OK):
            raise RuntimeError('Bad handshake: return code ' + handshake_return)
        has_connection = True
        break
    except:
        has_connection = False
        if time.clock() - start_time > MAX_TIME:
            print("Timed out after waiting {} seconds".format(MAX_TIME))
            break

#start client
while has_connection:
    move = raw_input('Ready to play: rock, paper or scissors?')
    while move not in MOVES: #error checking so we send a correct move to the server
        move = raw_input('Invalid move choice, try again:')
    utils.send_packet(client_server, move)
    print("Waiting for opponent...")
    received = utils.receive_packet(client_server)
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


