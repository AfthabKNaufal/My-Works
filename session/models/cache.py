from cachetools import cached
import time

s=time.time()

def old_fib(n):
    return n if n<2 else old_fib(n-1) + old_fib(n-2)

print(old_fib(35))
print("Time Taken: ", time.time() - s)




#cache
s = time.time()

@cached(cache={})
def old_fib(n):
    return n if n<2 else old_fib(n-1) + old_fib(n-2)

print(old_fib(35))
print("Time Taken: ", time.time() - s)