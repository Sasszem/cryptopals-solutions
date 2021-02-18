import itertools
import string

"""
Damn these challanges get hard FAST

"""


def hamming(first, second):
    assert len(first)==len(second), f"hamming called with diffing length inputs: {first}, {second}!"
    diff = bytes(a^b for a,b in zip(first, second))
    return sum(sum((a>>i)&1 for i in range(8)) for a in diff)

def normalized_hamming_pair(first, second, size):
    return hamming(first, second)/size

"""
The challenge description is just MISLEADING
if you only calculate the hamming of the first 2 blocks
you find that key len 5 is the winner
but nope, it's not
It suggests using a rolling window tho
"""
def normalized_hamming(text, size):
    rolling_sum = 0
    for i in range(len(text)//size - 1):
        base = size*i
        first = text[base:base+size]
        second = text[base+size:base+2*size]
        rolling_sum += normalized_hamming_pair(first, second, size)
    return rolling_sum / (len(text)//size - 1)

def best_guessed_key_lengths(text, candidate_count=5, r = range(2,60)):
    """Returns the best candidate_count key sizes based on increasing hamming length in text"""
    return list(itertools.islice(sorted(((size) for size in r), key=lambda e: normalized_hamming(text, e)),candidate_count))

def separate_components(text, keylen):
    components = [[] for i in range(keylen)]
    for i,c in enumerate(text):
        components[i%keylen].append(c)
    return [bytes(x) for x in components]


"""
This kinda shitty
see https://laconicwolf.com/2018/06/30/cryptopals-challenge-6-break-repeating-key-xor/ for a better one!
"""
def score_text(text):
    if any(chr(x) not in string.printable for x in text):
        return -1000
    return sum(chr(x) in string.ascii_lowercase for x in text) - sum(chr(x) in string.punctuation for x in text)

def xor_decode(msg, key):
    assert isinstance(msg, bytes)
    return bytes(map(lambda x: x^key, msg))

def solve_component(component):
    poss = list(map(ord, string.printable))
    return max(poss, key=lambda x: score_text(xor_decode(component, x)))

def decode_text(text, key):
    return bytes(a^b for a,b in zip(text, itertools.cycle(key)))


"""
I had a hard time with re-assembling the parts
until I gave up and copy-pasted the code that just decodes it with a key
I had the right key, but not checked if I had it
I just tried to play with the scoring function...
stupid me...
"""
def solve(msg):
    for keylen in best_guessed_key_lengths(msg, r=range(1,100)):
        print(f"LEN={keylen}")
        components = separate_components(msg, keylen)
        key = bytes([solve_component(c) for c in components])
        print(f"KEY='{key.decode()}'")
        print(decode_text(msg, key).decode())
        return # return so we only print the first
        # could print others if the key guess was wrong tho


if __name__=="__main__":
    # test hamming
    first = "this is a test".encode()
    second = "wokka wokka!!!".encode()
    assert hamming(first, second)==37

    from base64 import b64decode
    with open("6.txt") as f:
        raw = b64decode(f.read())

    solve(raw)