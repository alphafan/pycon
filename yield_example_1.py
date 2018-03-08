def count_down(n):
    while n > 0:
        yield n
        n -= 1


for i in count_down(5):
    print(i)

c = count_down(5)
print(next(c))
print(next(c))
print(next(c))
print(next(c))
print(next(c))
print(next(c))