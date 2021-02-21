class RNG:
    w, n, m, r = (32, 624, 397, 31)
    a = 0x9908B0DF
    #a = 0x9908b0df
    u, d = (11, 0xFFFFFFFF)
    s, b = (7, 0x9D2C5680)
    t, c = (15, 0xEFC60000)
    l = 18
    f = 1812433253

    lower_mask = (1<<r)-1;
    upper_mask = ((1<<w)-1)^lower_mask
    

    def __init__(self, seed):
        self.MT = [0 for _ in range(self.n)]
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            #self.MT[i] = self.lower_mask & (-self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i)
            temp = self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i
            self.MT[i] = temp & 0xffffffff
    def get(self):
        if self.index>=self.n:
            assert self.index==self.n, "Error: RNG was never seeded"
            # Should never hit that error since we seed in the constructor
            self.twist()
        
        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
    
        self.index += 1
        return y&0xffffffff

    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i+1)%self.n] & self.lower_mask)
            xA = x>>1
            if x%2 != 0:
                xA ^= self.a
            self.MT[i] = self.MT[(i+self.m)%self.n] ^ xA
        self.index = 0


if __name__=="__main__":
    R = RNG(0)
    for i in range(1000):
        print(R.get())