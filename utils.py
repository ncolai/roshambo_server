"""
Useful functions for handling proper TCP framing
Pulled from https://eli.thegreenplace.net/2011/08/02/length-prefix-framing-for-protocol-buffers
"""
import socket, struct, sys      #standard libraries

def send_packet(sock, data):
    """ Send a packet of data to a socket, prepended by its length packed in 4
        bytes (big endian).
    """
    packed_len = struct.pack('>L', len(data))
    sock.sendall(packed_len + data)

def receive_packet(sock):
    """ Read a packet from a socket.  """
    len_buf = socket_read_n(sock, 4)
    msg_len = struct.unpack('>L', len_buf)[0]
    msg_buf = socket_read_n(sock, int(msg_len))
    return msg_buf

def socket_read_n(sock, n):
    """ Read exactly n bytes from the socket.
        Raise RuntimeError if the connection closed before
        n bytes were read.
    """
    buf = ''
    while n > 0:
        data = sock.recv(n)
        if data == '':
            raise RuntimeError('unexpected connection close')
        buf += data
        n -= len(data)
    return buf
