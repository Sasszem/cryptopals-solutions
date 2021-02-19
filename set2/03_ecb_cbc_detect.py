from Crypto.Cipher import AES
from random import randrange, choice
import importlib
pad = importlib.import_module("01_padding").pad


def random_key():
    return bytes(randrange(256) for _ in range(16))

def encryption_black_box(text):
    key = random_key()
    message = pad(bytes(randrange(256) for _ in range(randrange(5,15))) + text + bytes(randrange(256) for _ in range(randrange(5,15))), 16)

    mode = choice(["CBC", "ECB"])
    if mode=="CBC":
        crypto = AES.new(key, AES.MODE_CBC, iv=random_key())
    else:
        crypto = AES.new(key, AES.MODE_ECB)
    return crypto.encrypt(message)

def decide(func):
    text = ("A"*256).encode()
    enc = func(text)
    blocks = [enc[i:i+16] for i in range(0,len(enc), 16)]
    if len(set(blocks)) < len(blocks)//2:
        return "ECB"
    return "CBC"

if __name__=="__main__":
    # we hook the random function
    # so we can peek inside the black box
    # for testing if the end result is correct

    RANDOM_VAR = 0
    choice = lambda x: x[RANDOM_VAR]

    for i in range(1000):
        RANDOM_VAR = randrange(2)
        assert decide(encryption_black_box)==["CBC","ECB"][RANDOM_VAR]

    print("Tests passed!")
