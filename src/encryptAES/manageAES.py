from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import json


with open("aes_keys.json", "r") as f:
    data = json.load(f)
    aes_key = base64.b64decode(data["key"])
    aes_iv  = base64.b64decode(data["iv"])


assert len(aes_key) in [16, 24, 32]
assert len(aes_iv) == 16

def encrypt(plaintext):
    json_data = json.dumps(plaintext).encode("utf-8")
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    encrypted = cipher.encrypt(pad(json_data, AES.block_size))
    return base64.b64encode(encrypted).decode("utf-8")

def decrypt(ciphertext):
    raw = base64.b64decode(ciphertext)
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    decrypted = unpad(cipher.decrypt(raw), AES.block_size)
    return json.loads(decrypted.decode("utf-8"))
