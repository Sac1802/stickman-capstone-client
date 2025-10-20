import socket
import threading
import time

import encryptAES.manageAES
import generate_rsa.generate_rsa

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 5005
key = ""
iv = ""
message = ""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(False)

def receive_message():
    global key, iv, message
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            message = data
            if b":" in data:
                parts = data.split(b":", 1)
                key = generate_rsa.generate_rsa.decrypt_rsa(parts[0])
                iv = generate_rsa.generate_rsa.decrypt_rsa(parts[1])
            return_value()
            print(f"Message received from {addr}: {data.decode()}")
        except BlockingIOError:
            time.sleep(0.01)
        except Exception as e:
            print(f"Error receiving: {e}")
            break


threading.Thread(target=receive_message, daemon=True).start()

def send_message(message: str):
    try:
        client_socket.sendto(message.encode(), (SERVER_ADDRESS, SERVER_PORT))
        print(f"Send: {message}")
    except Exception as e:
        print(f"Error to send: {e}")

def return_value():
    return encryptAES.manageAES.decrypt(message, key, iv)

def return_keys():
    return [key, iv]

def close_socket():
    client_socket.close()
    print("Socket close")
