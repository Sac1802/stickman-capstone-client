from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import json


def encrypt(plaintext, aes_key, aes_iv):
    json_data = json.dumps(plaintext).encode()
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    encrypted = cipher.encrypt(pad(json_data, AES.block_size))
    return base64.b64encode(encrypted)

def decrypt(ciphertext, aes_key, aes_iv):
    raw = base64.b64decode(ciphertext)
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    decrypted = unpad(cipher.decrypt(raw), AES.block_size)
    return json.loads(decrypted.decode())