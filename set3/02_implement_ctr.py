from Crypto.Cipher import AES

def num_to_bytes(num):
    return bytes([(num&(0xff<<(i*8)))>>(i*8) for i in range(8)])

def break_to_blocks(text):
    return [text[i:i+16] for i in range(0,len(text), 16)]

def block_xor(text, key):
    return bytes(a^b for a,b in zip(text, key))
def gen_mask(key, nonce, i):
    return AES.new(key, AES.MODE_ECB).encrypt(nonce + num_to_bytes(i))
def crypt_ctr(key, plaintext, nonce=b"\x00"*8):
    return b"".join(block_xor(block, gen_mask(key, nonce, i)) for i, block in enumerate(break_to_blocks(plaintext)))

if __name__=="__main__":
    from base64 import b64decode
    s = b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
    text = crypt_ctr(b"YELLOW SUBMARINE", s)
    print(text.decode())
    assert crypt_ctr(b"YELLOW SUBMARINE", text) == s