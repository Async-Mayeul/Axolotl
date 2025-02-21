import os
import base64
from Crypto.Cipher import AES
from Crypto import Random

class AESCipher:
    def __init__(self, key):
        self.key = base64.b64decode(key)
        self.bs = AES.block_size

    def pad(self, s):
        # Pads the text with null bytes to match the block size.
        return s + (self.bs - len(s) % self.bs) * "\x00"

    def unpad(self, s):
        s = s.decode("utf-8")
        return s.rstrip("\x00")

    def encrypt(self, raw):
        # Encrypts the raw text after padding, then returns the IV+ciphertext encoded in base64.
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode("utf-8")))

    def decrypt(self, enc):
        # Decodes the input, extracts the IV, decrypts, and unpads the plain text.
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain = cipher.decrypt(enc[16:])
        plain = self.unpad(plain)
        return plain

def ENCRYPT(PLAIN, KEY):
    cipher = AESCipher(KEY)
    enc = cipher.encrypt(PLAIN)
    return enc.decode()

def DECRYPT(ENC, KEY):
    cipher = AESCipher(KEY)
    dec = cipher.decrypt(ENC)
    return dec

def generateKey():
    # Generates a random 32-byte key, then encodes it in base64.
    key = base64.b64encode(os.urandom(32))
    return key.decode()
