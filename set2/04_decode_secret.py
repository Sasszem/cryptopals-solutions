from Crypto.Cipher import AES
from random import randrange
from base64 import b64decode
from importlib import import_module

pad = import_module("01_padding").pad


class Coder:
    secret = b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")

    def __init__(self):
        self.key = bytes(randrange(256) for _ in range(16))
        self.AES = AES.new(self.key, AES.MODE_ECB)

    def code(self, msg):
        return self.AES.encrypt(pad(msg+self.secret, 16))



def get_blocksize(coder):
    for possible_blocksize in range(4,256):
        enc = coder.code(("A"*8*possible_blocksize).encode())
        blocks = [enc[j:j+possible_blocksize] for j in range(0, len(enc), possible_blocksize)]
        if blocks[0]==blocks[1]==blocks[2]==blocks[3]:
            return possible_blocksize

def assert_ecb(coder, blocksize):
    enc = coder.code(("A"*blocksize*32).encode())
    blocks = [enc[j:j+blocksize] for j in range(0, len(enc), blocksize)]
    assert len(set(blocks))<len(blocks)*3/4

def solve(coder, blocksize, guessed_secret_len = 2000):
    secret = b""
    blen = len(pad(("A"*guessed_secret_len).encode(), blocksize))
    for i in range(guessed_secret_len):
        db = {}
        msg = (("A"*(blen-1-len(secret)))).encode()
        for byt in range(256):
            m = msg + secret + bytes([byt])
            last_block = coder.code(m)[len(m)-blocksize:len(m)]
            db[last_block] = byt
        enc = coder.code(msg)[len(m)-blocksize:len(m)]
        try:
            secret += bytes([db[enc]])
        except KeyError:
            assert(secret[-1]==1)
            return secret[:-1]
    # KeyError will occur if we can't decode
    # because the last byte changed
    # because it was a padding byte of 1
    # and it changed to a 2

if __name__=="__main__":
    coder = Coder()

    blocksize = get_blocksize(coder)
    assert_ecb(coder, blocksize)
    secret = solve(coder, blocksize)
    print(secret.decode())