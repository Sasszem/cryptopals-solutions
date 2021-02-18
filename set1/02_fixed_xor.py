def str_xor(bytes1: bytes, bytes2: bytes) -> bytes:
    assert len(bytes1)==len(bytes2), "Can't XOR two differenth length buffers!"
    return bytes(a^b for a, b in zip(bytes1, bytes2))

if __name__=="__main__":
    from binascii import unhexlify, hexlify
    a = unhexlify("1c0111001f010100061a024b53535009181c")
    b = unhexlify("686974207468652062756c6c277320657965")
    target = unhexlify("746865206b696420646f6e277420706c6179")
    assert str_xor(a,b)==target, "XOR decoding failed!"