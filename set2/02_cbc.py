from Crypto.Cipher import AES

def CBC(text, key, IV = bytes(0 for _ in range(16))):
    assert isinstance(text, bytes), "text should be bytes!"
    assert isinstance(key, bytes), "key should be bytes"
    assert isinstance(IV, bytes), "IV should be bytes"
    assert len(key)==16, "Key len should be 16!"
    state = IV
    res = bytes()
    decrypt = AES.new(key, AES.MODE_ECB)
    for i in range(len(text) // 16):
        block = text[i*16:i*16+16]
        blockres = bytes(a^b for a, b in zip(decrypt.decrypt(block), state))
        state = block
        res += blockres
    return res

if __name__=="__main__":
    from base64 import b64decode as bdec
    with open("10.txt") as f:
        print(CBC(bdec(f.read()), b"YELLOW SUBMARINE").decode())