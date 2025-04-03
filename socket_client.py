import socket
import sys
from dotenv import load_dotenv  
import os
from wizard_core import log

load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

if len(sys.argv) < 2:
    print("Usage: python socket_client.py <command>")
    sys.exit(1)

log(f"Connecting to {HOST}:{PORT}")

command = " ".join(sys.argv[1:])

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        log("sending command")
        s.connect((HOST, PORT))
        s.sendall(command.encode('utf-8'))

        response = s.recv(1024).decode('utf-8').strip()
        log(f"Response: {response}")


except ConnectionRefusedError:
    print("Connection refused. Please ensure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")

