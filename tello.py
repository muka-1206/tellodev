import socket

class Tellosocket:
    
    def __init__(self, pc_ip, pc_port, tello_ip="192.168.10.1", tello_port=8889):
        self.ip = tello_ip
        self.port = tello_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((pc_ip, pc_port))
        
    def send(self, msg):
        address = (self.ip, self.port)
        self.sock.sendto(msg.encode("utf-8"), address)

    def receive(self):
        chunk, address = self.sock.recvfrom(4096)
        return chunk.decode()

    def close(self):
        self.sock.close()