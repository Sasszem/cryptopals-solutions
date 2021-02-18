"""
Of course, we can just print all the 255 possibilities and rely on advanced optical language recognition (i.e a human looking at all of the lines spotting the one that makes sense), but we can filter the possibilities

For now, the message should:
- only contaion ASCII characters
- have at least one space

This just eleiminates most of the possibilities
"""

def check_msg(msg: bytes):
    return all(32<=x<127 for x in msg) and any(x==32 for x in msg)

def stringify_msg(msg):
    return "".join(map(chr, msg))

def decode_message(msg, key):
    return bytes(map(lambda x: x^key, msg))

def bruteforce_key(msg, check_msg):
    candidates = []
    for key in range(255):
        decoded = decode_message(msg, key)
        if check_msg(decoded):
            candidates.append((decoded, key))
    return candidates

if __name__=="__main__":
    from binascii import unhexlify
    message = unhexlify("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
    for msg, key in bruteforce_key(message, check_msg):
        print(msg, key)