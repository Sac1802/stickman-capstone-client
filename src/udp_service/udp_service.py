import socket
import threading
import time
import json
from encryptAES import manageAES

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 9876

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(False)
client_socket.bind(("", 0))

message_queue = []

def receive_message():
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            decrypted_str = manageAES.decrypt(data)
            message = json.loads(decrypted_str)
            message_queue.append(message)
        except BlockingIOError:
            time.sleep(0.01)
        except socket.error as e:
            if e.winerror == 10022:
                print("Error de socket: Argumento no válido. El servidor puede haberse cerrado o hay un problema de red.")
                time.sleep(1)
            else:
                print(f"Error de socket no manejado: {e}")
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
        # If the message is a dictionary, convert it to a JSON string
        if isinstance(message_to_send, dict):
            message_str = json.dumps(message_to_send)
        else:
            message_str = message_to_send

        encrypted = manageAES.encrypt(message_str)
        client_socket.sendto(encrypted, (SERVER_ADDRESS, SERVER_PORT))
    except Exception as e:
        print(f"Error Sending: {e}")

def close_socket():
    client_socket.close()
    print("Socket Close")