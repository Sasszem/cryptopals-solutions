# we need pycrypto(dome)
from Crypto.Cipher import AES
import base64


with open("7.txt") as f:
    raw = base64.b64decode(f.read())

key = "YELLOW SUBMARINE".encode()

cipher = AES.new(key, AES.MODE_ECB)
print(cipher.decrypt(raw).decode())