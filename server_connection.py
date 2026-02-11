import socket
import threading

def send_request(conn_id, host, port, message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"[{conn_id}] Connected. Sending request...")
            import socket
import threading
import sys

# Increase limit if you need more than 1000
sys.setrecursionlimit(50000000)

def spawn_connections_recursive(current, total, host, port):
    if current >= total:
        return

    # 1. Define the work for this specific connection
    def worker():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                print(f"Connected {current}")
                # Keep it open for a bit
                import time
                time.sleep(300000) 
        except Exception as e:
            print(f"Error on {current}: {e}")

    # 2. Start the thread (Parallelism)
    threading.Thread(target=worker).start()

    # 3. Recursive call for the next connection
    spawn_connections_recursive(current + 1, total, host, port)

# Usage
spawn_connections_recursive(0, 50000000, 'localhost', 8000)

            # Send the request data
            s.sendall(message.encode('utf-8'))
            
            # Optional: Receive a response from the server
            response = s.recv(1024)
            print(f"[{conn_id}] Server said: {response.decode('utf-8')}")
            
    except Exception as e:
        print(f"[{conn_id}] Error: {e}")

# Example: Spawning 5 connections that each send a request
for i in range(50000000):
    msg = f"GET /data_packet_{i} HTTP/1.1\r\n\r\n"
    threading.Thread(target=send_request, args=(i, 'localhost', 8000, msg)).start()
