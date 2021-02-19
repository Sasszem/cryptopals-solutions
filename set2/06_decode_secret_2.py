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
        self.base = bytes(randrange(256) for _ in range(20, 30))
        print(f"Padding: {len(self.base)}")

    def code(self, msg):
        return self.AES.encrypt(pad(self.base + msg+self.secret, 16))

def break_to_blocks(text, blocksize):
    return [text[j:j+blocksize] for j in range(0, len(text), blocksize)]

# this will crash if the two are the same
def remove_same(first, second):
    while first[0]==second[0]:
        first  = first[1:]
        second = second[1:]
    while first[-1]==second[-1]:
        first  = first[:-1]
        second = second[:-1]
    return first, second

def get_blocksize(coder):
    for possible_blocksize in range(4,256):
        blocks1 = break_to_blocks(coder.code(("A"*8*possible_blocksize).encode()), possible_blocksize)
        blocks2 = break_to_blocks(coder.code(("B"*8*possible_blocksize).encode()), possible_blocksize)
        blocks1, blocks2 = remove_same(blocks1, blocks2)
        if all(d == blocks1[1] for d in blocks1[1:-1]):
            return possible_blocksize

def assert_ecb(coder, blocksize):
    blocks = break_to_blocks(coder.code(("A"*blocksize*64).encode()), blocksize)
    assert len(set(blocks))<len(blocks)*3/4

def get_base_padding(coder, blocksize):
    for p in range(blocksize):
        blocks1 = break_to_blocks(coder.code(("X"*p + "A"*blocksize*16).encode()), blocksize)
        blocks2 = break_to_blocks(coder.code(("X"*p + "B"*blocksize*16).encode()), blocksize)
        blocks1, blocks2 = remove_same(blocks1, blocks2)
        if blocks1[0]==blocks1[1] and blocks2[0]==blocks2[1]:
            return p

def get_first_block_ofset(coder, blocksize):
    p = get_base_padding(coder, blocksize)
    blocks1 = break_to_blocks(coder.code(("X"*p + "A"*blocksize*16).encode()), blocksize)
    blocks2 = break_to_blocks(coder.code(("X"*p + "B"*blocksize*16).encode()), blocksize)
    for i, b1, b2 in zip(range(len(blocks1)), blocks1, blocks2):
        if b1!=b2:
            return i*blocksize, p

def solve(coder, blocksize, guessed_secret_len = 2000):
    ofset, p = get_first_block_ofset(coder, blocksize)
    secret = b""

    blen = len(pad(("A"*guessed_secret_len).encode(), blocksize))

    for i in range(guessed_secret_len):
        db = {}
        msg = (("A"*(blen-1-len(secret)))).encode()
        for byt in range(256):
            m = msg + secret + bytes([byt])
            last_block = coder.code(p*b"X" + m)[ofset + len(m)-blocksize:ofset + len(m)]
            db[last_block] = byt
        enc = coder.code(p*b"X" + msg)[ofset + len(m)-blocksize:ofset + len(m)]
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
    print(blocksize)
    assert_ecb(coder, blocksize)
    print(get_base_padding(coder, blocksize))
    print(get_first_block_ofset(coder, blocksize))
    secret = solve(coder, blocksize)
    print(secret.decode())