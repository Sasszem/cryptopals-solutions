
import time
import random
import importlib
RNG = importlib.import_module("05_implement_mersenne").RNG

random.seed(int(time.time()))

def gen_rand():
    time.sleep(random.randrange(40, 100))
    seed = int(time.time())
    R = RNG(seed)
    print(f"Seeded:\n{seed}")
    time.sleep(random.randrange(20, 200))
    return R.get()

def crack(r):
    t = int(time.time())
    print(f"Starting: {t}")
    print(f"Min: {t-3000}")
    for x in range(t-3000, t+10):
        if RNG(x).get() == r:
            return x

print(crack(gen_rand()))