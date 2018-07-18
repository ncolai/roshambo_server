#!/usr/bin/env python
import socket, select, sys
import random
import signal
from threading import Thread
from multiprocessing.pool import ThreadPool

#user defined libraries
import utils

MAX_CONNECTIONS =       5
MOVES           =       ['rock', 'paper', 'scissors']

#TODO: replace print 'xyz' with print 'xyz\n', (comma included) for thread safety
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

def ai_client(conn):
    '''Client for playing against computer'''
    while True:
        move = utils.receive_packet(conn)
        if move not in MOVES:
            conn.send('ERROR')
            break
        else:
            print(move + ' was sent')
            computer_move = roshambo_ai()
            status = roshambo_turn(MOVES.index(move), computer_move)
            print(status + ' ' + MOVES[computer_move])
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
            print(moves[0] + ' by P1, ' + moves[1] + ' by P2')
            status0 = roshambo_turn(MOVES.index(moves[0]), MOVES.index(moves[1]))
            status1 = roshambo_turn(MOVES.index(moves[1]), MOVES.index(moves[0]))
            print('P1 ' + status0 + ', P2 ' + status1)
            utils.send_packet(conn0, status0 + ' ' + moves[1])
            utils.send_packet(conn1, status1 + ' ' + moves[0])
    for conn in [conn0, conn1]:
        conn.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 9992

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    pool = ThreadPool(processes=MAX_CONNECTIONS)
    while True:
        conn0, addr0 = server.accept()
        conn1, addr1 = server.accept()
        pool.apply_async(matchup_client, (conn0,conn1,))
        #pool.apply_async(ai_client, (conn0,))

    server.close()
        

