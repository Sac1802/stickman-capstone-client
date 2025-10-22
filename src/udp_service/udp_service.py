import socket
import threading
import time
import json
from encryptAES import manageAES

SERVER_ADDRESS = "136.112.137.217"
SERVER_PORT = 9876

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(False)
client_socket.bind(("", 0))

message_queue = []
running = True

def receive_message():
    while running:
        try:
            data, addr = client_socket.recvfrom(4096)
            message = manageAES.decrypt(data)
            message_queue.append(message)
        except BlockingIOError:
            time.sleep(0.01)
        except socket.error as e:
            if hasattr(e, "winerror") and e.winerror == 10022:
                print("Error de socket: argumento no válido. El servidor puede haberse cerrado o hay un problema de red.")
                time.sleep(1)
            else:
                print(f"Socket error: {e}")
                time.sleep(0.5)
        except Exception as e:
            print(f"Error receiving or decrypting: {e}")
            pass

threading.Thread(target=receive_message, daemon=True).start()

def get_message():
    if message_queue:
        return message_queue.pop(0)
    return None

def send_message(message_to_send):
    try:
        encrypted = manageAES.encrypt(message_to_send)
        client_socket.sendto(encrypted.encode("utf-8"), (SERVER_ADDRESS, SERVER_PORT))
    except Exception as e:
        print(f"[ERROR] Sending message failed: {e.__class__.__name__} - {e}")

def close_socket():
    global running
    running = False
    client_socket.close()
    print("Socket closed")
