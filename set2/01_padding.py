def pad(msg, blocklen):
    diff = len(msg)%blocklen
    pad = blocklen - diff if diff else diff
    return msg + bytes([pad for _ in range(pad)])

if __name__=="__main__":
    print(pad("YELLOW SUBMARINE".encode(), 20))