from binascii import unhexlify
from base64 import b64encode

def convert(src):
    return b64encode(unhexlify(src)).decode()


if __name__=='__main__':
    src = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    dst = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    assert(convert(src)==dst)
