import socket
import threading
import time

class RingNode:
    def __init__(self, listen_ip, listen_port, next_ip, next_port, is_initiator=False):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.next_ip = next_ip
        self.next_port = next_port
        self.is_initiator = is_initiator
        self.running = True

    def start(self):
        listener_thread = threading.Thread(target=self.listen)
        listener_thread.start()
        if self.is_initiator:
            time.sleep(1)  
            self.send(1)

    def listen(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.listen_ip, self.listen_port))
        server_socket.listen(1)
        print(f"[{self.listen_ip}:{self.listen_port}] Listening...")

        while self.running:
            conn, addr = server_socket.accept()
            data = conn.recv(1024)
            if data:
                value = int(data.decode())
                print(f"[{self.listen_ip}:{self.listen_port}] Received: {value}")
                if value >= 100:
                    print(f"[{self.listen_ip}:{self.listen_port}] Value 100 reached, stopping.")
                    self.running = False
                else:
                    self.send(value + 1)
            conn.close()

    def send(self, value):
        success = False
        attempts = 0
        while not success and attempts < 10:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.next_ip, self.next_port))
                client_socket.send(str(value).encode())
                print(f"[{self.listen_ip}:{self.listen_port}] Sent: {value} to [{self.next_ip}:{self.next_port}]")
                client_socket.close()
                success = True
            except ConnectionRefusedError:
                print(f"[{self.listen_ip}:{self.listen_port}] Connection refused, retrying in 1 second...")
                attempts += 1
                time.sleep(1)
            except Exception as e:
                print(f"[{self.listen_ip}:{self.listen_port}] Unexpected error: {e}")
                break


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python ring_communication.py <node_number (1/2/3)>")
        sys.exit(1)

    node_number = int(sys.argv[1])

    if node_number == 1:
        node = RingNode('127.0.0.1', 5001, '127.0.0.2', 5002, is_initiator=True)
    elif node_number == 2:
        node = RingNode('127.0.0.2', 5002, '127.0.0.3', 5003)
    elif node_number == 3:
        node = RingNode('127.0.0.3', 5003, '127.0.0.1', 5001)
    else:
        print("Node number must be 1, 2 or 3.")
        sys.exit(1)

    node.start()
