import socket
import threading
import time

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 5005

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(False)

def receive_message():
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            print(f"Message send to {addr}: {data.decode()}")
        except BlockingIOError:
            time.sleep(0.01)
        except Exception as e:
            print(f"Error to receipt: {e}")
            break

threading.Thread(target=receive_message, daemon=True).start()

def send_message(message: str):
    try:
        client_socket.sendto(message.encode(), (SERVER_ADDRESS, SERVER_PORT))
        print(f"Send: {message}")
    except Exception as e:
        print(f"Error to send: {e}")

def close_socket():
    client_socket.close()
    print("Socket close")
