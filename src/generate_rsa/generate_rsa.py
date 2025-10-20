import base64
from Crypto.PublicKey import RSA
import os
from Crypto.Cipher import PKCS1_OAEP

def create_and_save_rsa_keypair(
    private_path="private.pem",
    public_path="public.pem",
    key_size=2048
):
    key = RSA.generate(key_size)

    private_key = key.export_key(format="PEM")
    public_key  = key.publickey().export_key(format="PEM")

    with open(private_path, "wb") as f:
        f.write(private_key)
    os.chmod(private_path, 0o600)

    with open(public_path, "wb") as f:
        f.write(public_key)

def get_private_key(path_private = "private.pem", passphrase=None):
    with open(path_private, "rb") as f:
        key = f.read()
    private_key = RSA.importKey(key, passphrase=passphrase)
    return private_key

def get_public_key(path_public = "public.pem"):
    with open(path_public, "rb") as f:
        public_key = f.read()
    public_key = RSA.importKey(public_key)
    return public_key

def decrypt_rsa(message):
    private_key = get_private_key()
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(message)
