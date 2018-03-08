from collections import deque


def count_down(n):
    while n > 0:
        yield n
        n -= 1


def run():
    while tasks:
        task = tasks.popleft()
        try:
            x = next(task)
            print(x)
            tasks.append(task)
        except StopIteration:
            print('Task')


tasks = deque()
tasks.extend([count_down(10), count_down(5), count_down(20)])
run()
