# Multi-Thread Fib micro service
#
# Command:
#
#   - start server
#   python server_simple.py
#
#   - Open a terminal
#   nc localhost 25000
#   10
#
#   - Open another terminal
#   nc localhost 25000
#   10
#   Crtl + C
#   python perf2.py
#
#   - Switch back to previous terminal
#   35

from fib import fib
from socket import *
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(4)


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print('Connection', addr)
        # fib_handler(client)
        Thread(target=fib_handler, args=(client,)).start()


def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        future = pool.submit(fib, n)
        result = future.result()
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print('Closed')


if __name__ == '__main__':
    fib_server(('', 25000))
