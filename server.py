from socket import *
import socket
from datetime import datetime
import threading
import logging

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                message = self.conn.recv(32)
                message = message.decode('utf-8')
                if message:
                    if message.startswith("TIME") and message.endswith("\r\n"):
                        response = "JAM " + datetime.strftime(datetime.now(), "%H:%M:%S") + "\r\n"
                        print(f"[SENDING] response to client {self.addr}")
                        self.conn.sendall(response.encode('utf-8'))
                    elif message.startswith("QUIT"):
                        print(f"[CLIENT EXIT] client from {self.addr} has exited. Bye bye!")
                        response = "invalid req\r\n"
                        self.conn.sendall(response.encode('utf-8'))
                    else:
                        print(f"[INVALID REQUEST] from {self.addr}")
                        self.conn.close()
                        break
            except OSError as e:
                pass
        self.conn.close()

class TimeServer(threading.Thread):
    def __init__(self):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        self.server_socket.bind(('localhost', 45000))
        self.server_socket.listen(1)
        while True:
            client_conn, client_addr = self.server_socket.accept()
            print(f"[CONNECTION] from {client_addr}")
            client_thread = ClientHandler(client_conn, client_addr)
            client_thread.start()
            self.clients.append(client_thread)

def start_server():
    server = TimeServer()
    server.start()

if __name__ == "__main__":
    start_server()
