#!/usr/bin/env python
import socket, select, sys
import random
import signal
from threading import Thread
from multiprocessing.pool import ThreadPool

MAX_BYTES       =       1024
MAX_CONNECTIONS =       5
MOVES           =       ['rock', 'paper', 'scissors']

#move_intval is the integer value of the PLAYER
#return win status of player
def roshambo_turn(conn, move_intval):
    '''Play one round of roshambo '''
    result = random.randint(0,2)
    if move_intval == result:
        return "DRAW", result
    elif move_intval == (result + 1) % 3:
        return "WIN", result
    else:
        return "LOSE", result

def roshambo_client(conn):
    while True:
        move = conn.recv(MAX_BYTES)
        if move in MOVES:
            print(move + ' was sent')
            status, result = roshambo_turn(conn, MOVES.index(move))
            print(status + ' ' + MOVES[result])
            conn.send(status + ' ' + MOVES[result])
        else:
            conn.send('ERROR')
            break
    conn.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 9992

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)

    pool = ThreadPool(processes=MAX_CONNECTIONS)
    while True:
        conn, addr = server.accept()
        pool.apply_async(roshambo_client, (conn,))

    server.close()
        

