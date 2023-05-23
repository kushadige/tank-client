from socket import AF_INET, SOCK_STREAM, SHUT_RDWR, socket, error
from threading import Thread
import traceback

class Client:
    def __init__(self):
        self.DEST_IP = "127.0.0.1"
        self.DEST_PORT = 4567
        self.BUF_SIZE = 1024
        self.DEST_ADDR = (self.DEST_IP, self.DEST_PORT)

        self.client = socket(AF_INET, SOCK_STREAM)
        self.connection_status = "waiting"

    def start(self):
        print("Welcome to TCP Tank - Multiplayer...")
        print("Trying to connect %s:%s" %self.DEST_ADDR)

        try:
            self.client.connect(self.DEST_ADDR)
        except error:
            traceback.print_exc()
            self.connection_status = "failure"
            self.client.close()
            return
        print("Connection successful... Press ESC to exit")
        self.connection_status = "success"

        # START NETWORK STREAM THREADS
        Thread(target=self.receive, args=(), daemon=True).start()
        Thread(target=self.send, args=(), daemon=True).start()

    def stop(self, msg=""):
        try:
            self.client.send("FIN".encode())
            self.client.shutdown(SHUT_RDWR)
            self.client.close()
            print(msg)
        except Exception as e:
            print(e)
        self.connection_status = "closed"

    def receive(self):
        while True:
            try:
                response = self.client.recv(self.BUF_SIZE).decode()
                if(response == "FIN"):
                    self.stop("Connection closed by server...")
                    break
                print(response)
            except error:
                self.connection_status = "closed"
                if self.connection_status == "waiting":
                    traceback.print_exc()
                break
        return
    
    def send(self):
        while True:
            try:
                response = input()
                if(response == "{exit}"):
                    self.stop("Connection closed by client...")
                    break
                self.client.send(response.encode())
            except error:
                self.connection_status = "closed"
                traceback.print_exc()
                break
        return