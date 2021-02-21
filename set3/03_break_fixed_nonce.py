import string

"""
Problem: upper/lowercase letters
If all characters are letters, upper/lowercase is 1 bitt difference
so we can't be sure if we got it right
"""

"""
This scoring is not perfect
but kinda works
"""
def score(text):
    return 2*sum(chr(x) in string.printable for x in text) - sum(chr(x) in string.punctuation for x in text)

def guess_key_byte(texts, b):
    c = [(bytes(t[b]^i for t in texts), i) for i in range(256)]
    return max(c, key=lambda x: score(x[0]))[1]

def solve(texts):
    kstream = [guess_key_byte(texts, i) for i in range(min(len(c) for c in texts))]
    return [bytes(a^b for a,b in zip(e, kstream)) for e in texts]

if __name__=="__main__":
    from base64 import b64decode
    from Crypto.Cipher import AES
    from random import randrange


    TEXTS = """
        SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==
        Q29taW5nIHdpdGggdml2aWQgZmFjZXM=
        RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==
        RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=
        SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk
        T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==
        T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=
        UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==
        QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=
        T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl
        VG8gcGxlYXNlIGEgY29tcGFuaW9u
        QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==
        QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=
        QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==
        QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=
        QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=
        VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==
        SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==
        SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==
        VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==
        V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==
        V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==
        U2hlIHJvZGUgdG8gaGFycmllcnM/
        VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=
        QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=
        VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=
        V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=
        SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==
        U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==
        U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=
        VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==
        QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu
        SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=
        VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs
        WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=
        SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0
        SW4gdGhlIGNhc3VhbCBjb21lZHk7
        SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=
        VHJhbnNmb3JtZWQgdXR0ZXJseTo=
        QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=
    """.split("\n")[1:-1] # remove first empty

    
    KEY = bytes(randrange(256) for _ in range(16))
    
    def encrypt(key, text, nonce = b"\x00"*8):
        return AES.new(key, AES.MODE_CTR, nonce=nonce).encrypt(text)
    
    ENC = [encrypt(KEY, b64decode(t.strip())) for t in TEXTS]
    #print(set(map(len, ENC)))


    for p in solve(ENC):
        print(p.decode())
#print(ENC[0][0]^b64decode(TEXTS[0])[0])