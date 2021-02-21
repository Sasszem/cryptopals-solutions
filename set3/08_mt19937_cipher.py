import time
import random
import importlib
RNG = importlib.import_module("05_implement_mersenne").RNG

def num_to_bytes(num):
    return bytes([(num&(0xff<<(i*8)))>>(i*8) for i in range(4)])

def crypt_mt19937(key, msg):
    assert key<2**16
    R = RNG(key)
    text =  msg
    blocks = [text[i:i+4] for i in range(0, len(text), 4)]
    keys = [num_to_bytes(R.get()) for _ in range(len(blocks))]
    coded = [bytes(a^b for a,b in zip(k,t)) for k,t in zip(keys, blocks)]
    return b"".join(coded)

def encrypt(key, msg):
    return crypt_mt19937(key, bytes(random.randrange(256) for _ in range(random.randrange(5,20)))+msg)


def solve(enc):
    for key in range(2**16):
        if b"AAAAAAAA" in crypt_mt19937(key, enc):
            return key

if __name__=="__main__":
    random.seed(int(time.time()))
    key = random.randrange(2**16)

    msg = b"A"*32
    enc = encrypt(key, msg)
    
    k = solve(enc)
    print(f"Found key: {k}")
    print(crypt_mt19937(k, enc))
    print(f"(key was: {key})")

    # Lesson learned, don't use 16 bit keys cuz' they get bruteforced in SECONDS