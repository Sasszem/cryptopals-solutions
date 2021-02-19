import string

"""
We can only validate padding if the plaintext is NOT arbitrary binary
Since otherwise we might want to send data that's incorrectly "padded"
and also if we want to send the text
"123456789012345\n" that would also look like bad padding
also
"123456\n\n\n\n\n\n\n\n\n\n" (10*\n) can be a valid padding OR a valid text
"""
def validate_padding(str, blocksize = 16):
    assert len(str)%blocksize==0, "STR len is not an integer multiple of blocksize"
    if str[-1]<blocksize:
        if all(d==str[-1] for d in str[-str[-1]:]):
            return str[:-str[-1]].decode()
    assert all(x in string.printable for x in str.decode()), "string contains binary data"

if __name__=="__main__":
    assert validate_padding(b"ICE ICE BABY\x04\x04\x04\x04")=="ICE ICE BABY"
    ERROR = False
    try:
        validate_padding(b"ICE ICE BABY\x01\x02\x03\x04")
        validate_padding(b"ICE ICE BABY\x05\x05\x05\x05")

        ERROR = True # we should never reach this line
    except:
        pass
    assert not ERROR