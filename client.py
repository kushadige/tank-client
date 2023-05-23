import json
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR, socket, error
from threading import Thread
import traceback

from constants import *

class Client:
    def __init__(self):
        self.DEST_IP = "127.0.0.1"
        self.DEST_PORT = 4567
        self.BUFFER_SIZE = 1024
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
        print("Connection successful...")
        self.connection_status = "success"

        # START NETWORK STREAM THREAD
        Thread(target=self.receive, args=(), daemon=True).start()

    def stop(self, msg=""):
        try:
            self.send(QUIT)
            self.client.close()
            if msg:
                print(msg)
        except Exception as e:
            print(e)
        self.connection_status = "closed"

    def receive(self):
        while True:
            try:
                data = self.client.recv(self.BUFFER_SIZE)
                if data:
                    response = json.loads(data)
                    code = response["code"]
                    if(code == CRASH):
                        self.stop("Connection closed by server...")
                        break
                    print(response)
            except error:
                self.connection_status = "closed"
                if self.connection_status == "waiting":
                    traceback.print_exc()
                break
        return
    
    def send(self, command, data={}):
        response = Client.encode({
            "command": command,
            "data": data
        })
        try:
            self.client.send(response)
            print("Sended: " + response.decode())
        except error:
            traceback.print_exc()
            print("Couldn't send: " + response.decode())

    def login(self, username, password):
        if username and password:
            data = {
                "username": username,
                "password": password
            }
            self.send(LOG, data)

    def register(self, username, password, confirm):
        if username and password and confirm and (password == confirm):
            data = {
                "username": username,
                "password": password
            }
            self.send(REG, data)

    @staticmethod
    def encode(data):
        plain_str = json.dumps(data, default=Client.obj_dict)
        encoded_str = plain_str.encode()
        return encoded_str
    @staticmethod
    def obj_dict(obj):
        return obj.__dict__
