"""
Tactic: if the line contains a repeating 16-byte block, it's sus
We only get one suspect, so I guess it works...
"""


def check(line):
    blocks = [line[s:s+16] for s in range(0, len(line), 16)]
    if len(set(blocks))<len(blocks):
        return True

with open("8.txt") as f:
    for i,line in enumerate(f):
        if check(line):
            print(f"line {i} sus:")
            print(f"\t'{line}'")
