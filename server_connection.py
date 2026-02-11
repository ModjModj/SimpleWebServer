import socket
import threading

def send_request(conn_id, host, port, message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"[{conn_id}] Connected. Sending request...")
            
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
