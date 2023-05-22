from socket import AF_INET, SOCK_STREAM, SHUT_RDWR, socket
from threading import Thread

class Client:
    def __init__(self):
        self.DEST_IP = "127.0.0.1"
        self.DEST_PORT = 4567
        self.BUF_SIZE = 1024
        self.DEST_ADDR = (self.DEST_IP, self.DEST_PORT)

        self.client = socket(AF_INET, SOCK_STREAM)
        self.server_down = False

    def start(self, scene):
        print("Welcome to Two Dot - Multiplayer... Trying to connect %s:%s" %self.DEST_ADDR)
        try:
            self.client.connect(self.DEST_ADDR)
        except:
            print("Could not connect to server...")
            scene.connection_status = "failure"
            self.client.close()
            quit()

        print("Connection was successful... Press ESC to exit")
        scene.connection_status = "success"
        Thread(target=self.receive_msg, args=(), daemon=True).start()
        Thread(target=self.send_msg, args=(), daemon=True).start()

    def receive_msg(self):
        while True:
            try:
                recvd_message = self.client.recv(self.BUF_SIZE).decode()
                if(recvd_message == "FIN"):
                    self.server_down = True
                    print("Connection closed...")
                    break
                print(recvd_message)
            except:
                break
    
    def send_msg(self):
        while True:
            try:
                msg = input()
                self.client.send(msg.encode())
            except:
                self.server_down = True
                break

    def close_active_sock(self):
        try:
            self.client.send("FIN".encode())
            self.client.shutdown(SHUT_RDWR)
            self.client.close()
        except:
            pass