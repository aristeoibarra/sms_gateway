import socket
import threading
import pickle
import time

from main import send

SERVER_HOST = ''
SERVER_PORT = 9000
BUFFER_SIZE = 1024 * 1024


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def handle_client(client_socket, client_address):
    print(f"{client_address[0]}:{client_address[1]} Connected!")

    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            data = pickle.loads(data)

            message = data['message']
            numbers = data['numbers']

            for x in numbers:
                send(x, message)
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()


def start_server():
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.listen()

    print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

    while True:
        try:
            client_socket, client_address = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except Exception as e:
            print(f"Error: {e}")

    s.close()


while True:
    try:
        local_ip = get_local_ip()
        SERVER_HOST = local_ip
        start_server()
    except Exception as e:
        print(f"Error: {e}")
        print("Restarting server in 5 seconds...")
        time.sleep(5)
