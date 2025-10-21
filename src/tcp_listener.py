import threading
import json
import base64
import socket
import queue # Import the queue module
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class TcpListener(threading.Thread):
    def __init__(self, game, client_socket, aes_key, aes_iv, message_queue):
        super().__init__()
        self.game = game
        self.client_socket = client_socket
        self.aes_key = aes_key
        self.aes_iv = aes_iv
        self.message_queue = message_queue
        self.running = True

    def decrypt_aes(self, encrypted_b64, key, iv):
        ciphertext = base64.b64decode(encrypted_b64)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode()

    def run(self):
        self.client_socket.settimeout(1.0) # Set a timeout for recv()
        while self.running:
            try:
                data = b""
                while True:
                    try:
                        chunk = self.client_socket.recv(4096)
                        if not chunk:
                            self.running = False
                            break
                        data += chunk
                        if b"\n" in data:
                            break
                    except socket.timeout:
                        # No data received within the timeout, continue loop to check self.running
                        break
                
                if not self.running or not data:
                    continue

                print(f"[TCP Listener] Received raw data: {data.decode().strip()}")
                encrypted_b64 = data.decode().strip()
                decrypted_json = self.decrypt_aes(encrypted_b64, self.aes_key, self.aes_iv)
                message = json.loads(decrypted_json)
                
                print(f"[TCP Listener] Received decrypted message: {message}")

                # Put the message into the queue for the main thread to process
                self.message_queue.put(message)

            except Exception as e:
                print(f"[TCP Listener] Error: {e}")
                self.running = False
        
        print("[TCP Listener] Listener stopped.")
        self.client_socket.close()

    def stop(self):
        self.running = False
