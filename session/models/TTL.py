from cachetools import cached, TTLCache
import time

@cached(cache=TTLCache(maxsize=3,ttl=5))
def myfun(n):

    s=time.time()
    time.sleep(n)

    print("\n Time Taken: ", time.time() - s)
    return (f"I am executed : {n}")

print(myfun(3))
print(myfun(3))
time.sleep(6)
print(myfun(3))