"""
Basically I've done it already in 03
"""

import base64
import importlib
solve = importlib.import_module("03_break_fixed_nonce").solve

with open("20.txt") as f:
    ENC = [base64.b64decode(x) for x in f]

for p in solve(ENC):
    print(p.decode())