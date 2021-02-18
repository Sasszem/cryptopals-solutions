import string

# have 2 do this cuz the naming :(
from importlib import import_module
bruteforce_key = import_module("03_fixed_byte_xor").bruteforce_key


"""
Finding that it has a \n at the end was hard, I assumed that it only contains chars 32-126...
"""
def check_msg(msg):
    return all((chr(x) in string.printable) for x in msg) and sum((chr(x) in string.punctuation) for x in msg) < len(msg)//5 and sum(x==ord(" ") for x in msg)


def find_all_candidates(strings):
    ret = []
    for c in strings:
        ret += bruteforce_key(c, check_msg)
    return ret

def pretty_print_finds(finds):
    for l in finds:
        print(*l)



if __name__=="__main__":
    from binascii import unhexlify
    with open("4.txt") as f:
        strings = [unhexlify(l.strip()) for l in f if len(l.strip())==60]
    pretty_print_finds(find_all_candidates(strings))