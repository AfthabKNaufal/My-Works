from cachetools import cached, RRCache
import time

@cached(cache=RRCache(maxsize=3))
def myfun(n):

    s=time.time()
    time.sleep(n)

    print("\n Time Taken: ", time.time() - s)
    return (f"I am executed : {n}")


print(myfun(3))
print(myfun(3))
print(myfun(2))
print(myfun(4))
print(myfun(1))
print(myfun(5))
print(myfun(3))