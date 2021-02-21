from Crypto.Cipher import AES
from random import randrange, choice
import string
import base64

class Challenge:
    def __init__(self):
        self.key = bytes(randrange(256) for _ in range(16))
        self.iv = b"abcdefghijklmopq"

    @staticmethod
    def _pad(msg):
        d = 16 - len(msg)%16
        return msg + bytes(d for _ in range(d))

    @staticmethod
    def _checkpad(msg):
        return msg[-msg[-1]:]==bytes([msg[-1]])*msg[-1]

    def getMessage(self):
        plaintext = self._pad("".join(choice(string.printable) for _ in range(randrange(100,200))).encode())
        return self.iv + AES.new(self.key, AES.MODE_CBC, iv=self.iv).encrypt(plaintext)

    def win(self, msg, encoded):
        return self.decrypt(encoded) == msg

    def decrypt(self, encoded):
        return AES.new(self.key, AES.MODE_CBC, iv=encoded[:16]).decrypt(encoded[16:])

    def oracle(self, encoded):
        return self._checkpad(self.decrypt(encoded))

def break_to_blocks(text):
    return [text[i:i+16] for i in range(0, len(text), 16)]

def solve_last_block(challenge, text):
    data = list(text)
    solved = b""
    while len(solved)<16:
        for i in range(256):
            data2 = data[:]
            for j,s in enumerate(solved):
                data2[-17-j] ^= s ^ (len(solved)+1)
            data2[-17-len(solved)] ^= i
            if len(solved)<15:
                data2[-18-len(solved)] ^= 255
            if challenge.oracle(bytes(data2)):
                solved += bytes([i^(len(solved)+1)])
                break
    return solved

def solve(challenge, text):
    solved = b""
    while len(text)>=32:
        solved += solve_last_block(challenge, text)
        text = text[:-16]
    return solved[::-1]

if __name__=="__main__":
    c = Challenge()
    m = c.getMessage()
    #assert c.oracle(m)
    print(break_to_blocks(c.decrypt(m)))
    print(break_to_blocks(solve(c,m)))
