import socket

def check_connection(host, port):
    try:
        with socket.create_connection((host, port), timeout=10):
            print(f"Connection to {host}:{port} successful")
    except Exception as e:
        print(f"Connection to {host}:{port} failed: {e}")

