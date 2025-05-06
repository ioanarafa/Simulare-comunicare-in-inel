This project simulates communication within a ring topology using three nodes, implemented in Python. Each node is configured to send and receive data using TCP sockets over the loopback IP addresses (127.0.0.x). The system demonstrates how a numeric value circulates around the ring and increments at each step until it reaches a threshold of 100.

    Project Components
Topology: A circular (ring) topology with three interconnected nodes:

Node 1: 127.0.0.1:5001 → Node 2: 127.0.0.2:5002

Node 2: 127.0.0.2:5002 → Node 3: 127.0.0.3:5003

Node 3: 127.0.0.3:5003 → Node 1: 127.0.0.1:5001

Initiator: Node 1 begins the simulation by sending the initial value 1.

Communication Logic:

Each node listens for incoming messages on a specific port.

Upon receiving a value, the node increments it by 1 and forwards it to the next node.

The process stops once the value reaches or exceeds 100.
