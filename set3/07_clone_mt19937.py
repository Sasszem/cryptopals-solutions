
import time
import importlib
RNG = importlib.import_module("05_implement_mersenne").RNG




def untemper(val):
    w, n, m, r = (32, 624, 397, 31)
    a = 0x9908B0DF
    #a = 0x9908b0df
    u, d = (11, 0xFFFFFFFF)
    s, b = (7, 0x9D2C5680)
    t, c = (15, 0xEFC60000)
    l = 18
    f = 1812433253

    y = val

    y = y ^ (y >> l)
    y = y ^ ((y << t) & c)

    # TODO: find out why we need exactly 7 and 3 runs, and not just 1
    for _ in range(7):
        y = y ^ ((y << s) & b)

    for _ in range(3):
        y = y ^ ((y >> u) & d)

    return y

R = RNG(int(time.time()))

R2 = RNG(0)
R2.MT = [untemper(R.get()) for _ in range(624)]

# the RNG is now cloned, both will generate the same values

for i in range(10):
    print(R.get(), R2.get())