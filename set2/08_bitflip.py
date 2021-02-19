from Crypto.Cipher import AES
from importlib import import_module
pad = import_module("01_padding").pad


KEY = b"42"*8
IV = b"\x69"*16

def code_data(data):
    msg = b"comment1=cooking%20MCs;userdata=" + data.replace(";", "%3b").replace("=", "%3d").encode() + b";comment2=%20like%20a%20pound%20of%20bacon"
    return AES.new(KEY, AES.MODE_CBC, iv=IV).encrypt(pad(msg, 16))

def is_admin(data):
    print(AES.new(KEY, AES.MODE_CBC, iv=IV).decrypt(data))
    return b";admin=true;" in AES.new(KEY, AES.MODE_CBC, iv=IV).decrypt(data)

if __name__=="__main__":
    # we could have used some analysis to decide how many bytes do we have to use
    # but we already know the blocksize, so...
    d = code_data("0"*2000)
    # huge data, we can just pick the middle to write...
    d = list(d)
    for i,x in enumerate(";admin=true;"):
        d[1120+i] ^= ord(x) ^ ord("0")
    print(is_admin(bytes(d)))