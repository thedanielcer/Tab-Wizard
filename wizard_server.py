import socket
import threading
from command_handler import handle_command
from dotenv import load_dotenv  
import os

load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

def handle_client_connection(conn, addr):
    print(f"[CONNECTED] {addr}")
    try:
        data = conn.recv(1024).decode('utf-8').strip()
        print(f"[RECEIVED] {data}")
        if data:
            handle_command(data)
        conn.sendall(b"OK")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

def start_server():
    print(f"[LISTENING] {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
