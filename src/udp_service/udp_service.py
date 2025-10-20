import socket
import threading
import time
from encryptAES import manageAES

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 5005

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(False)

def receive_message():
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            decrypted = manageAES.decrypt(data)
            print(f"Message receipt to {addr}: {decrypted}")
        except BlockingIOError:
            time.sleep(0.01)
        except Exception as e:
            print(f"Error receipt: {e}")
            break

threading.Thread(target=receive_message, daemon=True).start()

def send_message(messageSend: str):
    try:
        encrypted = manageAES.encrypt(messageSend)
        client_socket.sendto(encrypted, (SERVER_ADDRESS, SERVER_PORT))
        print(f"Message Send: {messageSend}")
    except Exception as e:
        print(f"Error Send: {e}")

def close_socket():
    client_socket.close()
    print("Socket Close")
