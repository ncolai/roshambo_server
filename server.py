#!/usr/bin/env python
import socket, select, sys, random
from multiprocessing.pool import ThreadPool

#user defined libraries
import utils
from utils import HandshakeCode

HOST            =       "localhost"
PORT            =       9990
MAX_CONNECTIONS =       5
MOVES           =       ['rock', 'paper', 'scissors']
SUPPORTED_PROTOCOLS =   [i for i in range(1,3)]

def roshambo_ai(): 
    '''Simple computer logic to play roshambo'''
    return random.randint(0,2)

def roshambo_turn(move1, move2):
    '''Play one round of roshambo, and return win status of P1'''
    if move1 == move2:
        return "DRAW"
    elif move1 == (move2 + 1) % 3:
        return "WIN"
    else:
        return "LOSE"

def handshake(conn, num_connections): #the networking version of sanity check
    '''True if successful handshake, and false if not'''
    protocol = utils.receive_packet(conn)
    if int(protocol) not in SUPPORTED_PROTOCOLS:
        utils.send_packet(conn, HandshakeCode.PROTOCOL_NOT_SUPPORTED)
    elif num_connections >= MAX_CONNECTIONS:
        utils.send_packet(conn, HandshakeCode.SERVER_FULL)
    else:
        utils.send_packet(conn, HandshakeCode.HANDSHAKE_OK)
        return True
    conn.close() #close connection if it's bad
    return False

def ai_client(conn):
    '''Client for playing against computer'''
    while True:
        move = utils.receive_packet(conn)
        if move not in MOVES:
            conn.send('ERROR')
            break
        else:
            utils.print_r(move + ' was sent')
            computer_move = roshambo_ai()
            status = roshambo_turn(MOVES.index(move), computer_move)
            utils.print_r(status + ' ' + MOVES[computer_move])
            utils.send_packet(conn, status + ' ' + MOVES[computer_move])
    conn.close()

def matchup_client(conn0, conn1):
    '''Client for two players playing against each other'''
    while True: 
        #TODO: add a condition variable/semaphore to coordinate receiving bytes together
        moves = [utils.receive_packet(conn) for conn in [conn0, conn1]]
        if moves[0] not in MOVES and moves[1] not in MOVES:
            break
        elif moves[0] not in MOVES:
            moves[0].send('ERROR')
        elif moves[1] not in MOVES:
            moves[1].send('ERROR')
        else:
            utils.print_r(moves[0] + ' by P1, ' + moves[1] + ' by P2')
            status0 = roshambo_turn(MOVES.index(moves[0]), MOVES.index(moves[1]))
            status1 = roshambo_turn(MOVES.index(moves[1]), MOVES.index(moves[0]))
            utils.print_r('P1 ' + status0 + ', P2 ' + status1)
            utils.send_packet(conn0, status0 + ' ' + moves[1])
            utils.send_packet(conn1, status1 + ' ' + moves[0])
    for conn in [conn0, conn1]:
        conn.close()

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    pool = ThreadPool(processes=MAX_CONNECTIONS)
    num_connections = 0 #TODO: make handshake recognize number of connections
    while True:
        conn0, addr0 = server.accept()
        handshake(conn0, num_connections)
        #conn1, addr1 = server.accept()
        #pool.apply_async(matchup_client, (conn0,conn1,))
        pool.apply_async(ai_client, (conn0,))

    server.close()
        

