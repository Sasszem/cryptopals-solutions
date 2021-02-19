from Crypto.Cipher import AES
from random import randrange

def parse_str(str):
    return {m[0]:m[1] for m in [d.split("=") for d in str.split("&")]}

def satanize(str):
    return str.replace("&","").replace("=","")

def profile_for(email, id=0, role='user'):
    return "&".join(f"{x}={satanize(y)}" for x, y in zip("email;uid;role".split(";"), [email, str(id), role]))

class ProfileCoder:
    def __init__(self):
        self.key = bytes(randrange(256) for _ in range(16))
        self.AES = AES.new(key, AES.MODE_ECB)
    def encrypt(self, profile):
        return self.AES.encrypt(profile.encode())
    def decrypt(self, profile):
        return parse_str(self.AES.decrypt(profile).decode())
    def admin_profile(self):
        return self.encrypt(profile_for("admin@admin.com", 0, 'admin'))

if __name__=="__main__":
    #print(parse_str("foo=bar&baz=quz&zap=zazzle"))
    print(profile_for("example@me.com"))