# Simple Fib micro service
#
# Command:
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
#


from fib import fib
from socket import *
from collections import deque
from select import select


tasks = deque()
recv_wait = {}  # Mapping sockets --> tasks(generators)
send_wait = {}  # Mapping sockets --> tasks(generators)


def run():
    while any([tasks, recv_wait, send_wait]):
        while not tasks:
            # No active tasks to run
            # Wait for I/O
            can_recv, can_send, _ = select(recv_wait, send_wait, [])
            for i, s in enumerate(can_recv):
                tasks.append(can_recv.pop(i))
            for i, s in enumerate(can_send):
                tasks.append(can_send.pop(s))
        task = tasks.popleft()
        try:
            why, what = next(task)  # Run to the yield
            if why == 'recv':
                # Must go wait somewhere
                recv_wait[what] = task
            elif why == 'send':
                send_wait[what] = task
            else:
                raise RuntimeError("ARG!")
        except StopIteration:
            print('Task done')


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        yield 'recv', sock
        client, addr = sock.accept()    # blocking
        print('Connection', addr)
        tasks.append(fib_handler(client))


def fib_handler(client):
    while True:
        yield 'recv', client
        req = client.recv(100)  # blocking
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        yield 'send', client
        client.send(resp)   # blocking
    print('Closed')


if __name__ == '__main__':
    tasks.append(fib_server(('', 25000)))
    print(tasks)
    run()
    print(tasks)
    print(recv_wait)
    print(send_wait)
