import pygame, traceback, json, random
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from core.game.tank import Tank
from core.globals import SCREEN_WIDTH, SCREEN_HEIGHT

from util.functions import encode

class Client:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.ADDR = (HOST, PORT)
        self.BUFFER_SIZE = 1024
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.status = "closed" # closed | waiting | connected
        
        self.users        = []  # lobbyde gerekli - chatleşme
        self.rooms        = []  # lobbyde gerekli - room_idler..
        self.active_room  = {
            "room_name": None,
            "players": [],
            "settings": {}
        }
        self.user         = {"username": "", "score": None}  # username score  - lobby ve game screende gerekli

        self.player_id    = None  # room ve game screende gerekli
        self.tank         = Tank("assets/body.png", random.randrange(42, SCREEN_WIDTH - 42), random.randrange(46, SCREEN_HEIGHT - 46), None, self)
        self.tank_group   = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()

        self.login_status = None # waiting | failure | success
        self.login_msg    = None

        self.game_started = False

    def login(self, username, password):
        ####### SEND LOGIN REQUEST TO SERVER  #######
        self.login_status = "waiting"
        self.login_msg    = "Waiting.."
        reply = {
            "command": "LOGN",
            "data": {
                "username": username,
                "password": password
            }
        }
        self.send(reply)
        #############################################
    
    def logout(self):
        ###### SEND LOGOUT REQUEST TO SERVER  ######
        reply = {
            "command": "LOGT",
            "data": {
                "username": self.user["username"]
            }
        }
        self.login_status = None
        self.login_msg    = None
        self.game_started = False
        self.user         = {"username": "", "score": None}
        self.send(reply)
        #############################################

    def create_room(self, room_name):
        ####### SEND CRTR REQUEST TO SERVER  #######
        reply = {
            "command": "CRTR",
            "data": {
                "room_name": room_name,
                "settings": {}
            }
        }
        self.send(reply)
        #############################################

    def enter_room(self, room_name):
        ####### SEND ENTER ROOM REQUEST TO SERVER  #######
        reply = {
            "command": "ENTR",
            "data": {
                "room_name": room_name,
                "player": {
                    "user": self.user,
                    "player_id": self.player_id,
                    "direction": self.tank.direction,
                    "pos": str(self.player_id) + ":" + str(self.tank.rect.centerx) + "," + str(self.tank.rect.centery)
                }
            }
        }
        self.send(reply)
        #############################################

    def leave_room(self):
        ####### SEND LEAVE ROOM REQUEST TO SERVER  #######
        reply = {
            "command": "LVER",
            "data": {
                "room_name": self.active_room["room_name"],
                "player_id": self.player_id
            }
        }
        self.tank         = Tank("assets/body.png", random.randrange(42, SCREEN_WIDTH - 42), random.randrange(46, SCREEN_HEIGHT - 46), None, self)
        self.tank_group   = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.game_started = False
        self.send(reply)
        self.player_id   = None
        self.active_room = {
            "room_name": None,
            "players": [],
            "settings": {}
        }
        #############################################

    def start_game(self):
        ####### SEND START GAME REQUEST TO SERVER  #######
        reply = {
            "command": "SRTG",
            "data": {
                "room_name": self.active_room["room_name"]
            }
        }
        self.send(reply)
        #############################################


    def message(self, message):
        ########### SEND MESSAGE TO CHAT ############
        reply = {
            "command": "MESG",
            "data": {
                "username": self.user["username"],
                "message": message
            }
        }
        self.send(reply)
        #############################################

    def start(self):
        #### Start Connection
        try:
            self.status = "waiting"
            self.socket.connect(self.ADDR)
            self.status = "connected"
            Thread(target=self.recv).start()
        except:
            traceback.print_exc()
            self.status = "closed"
            print("Server is unable...")

    def stop(self, closed_by_server: bool = False):
        if self.status != "closed":
            if closed_by_server:
                self.socket.close()
            else:
                reply = {
                    "command": "EXIT",
                    "data": {
                        "player_id": self.player_id,
                        "username": self.user["username"]
                    }
                }
                self.send(reply)
            self.status = "closed"

    def send(self, data):
        if self.status != "closed":
            self.socket.send(encode(data))

    def recv(self):
        while True:
            try:
                reply = self.socket.recv(self.BUFFER_SIZE)
                reply_organized = self.organize_string_data(reply.decode())
                if reply_organized:
                    try:
                        rp = json.loads(reply_organized)
                        print("[RECIEVED]", rp)
                        command = rp["command"]
                        if command == "DOWN": # Connection closed by server
                            self.stop(True)
                            break
                        if command == "INIT":
                            self.users = rp["data"]["users"]
                            self.rooms = rp["data"]["rooms"]
                        if command == "LOGN":
                            code, message = rp["data"]["code"], rp["data"]["message"]
                            if code == 400:
                                self.login_status = "failure"
                            elif code == 200:
                                self.login_status = "success"
                                self.user         = rp["data"]["user"]
                            self.login_msg = message
                        if command == "ENTL":
                            # User enters lobby
                            user = rp["data"]["user"]
                            if user:
                                self.users.append(user)
                        if command == "LVEL":
                            # User leaves lobby
                            username = rp["data"]["username"]
                            if username:
                                for i, user in enumerate(self.users):
                                    if user["username"] == username:
                                        self.users.remove(self.users[i])
                                        break
                        if command == "CRTR":
                            pass
                        if command == "ENTR": 
                            # Server Respond for Enter Room request.
                            """
                            {
                                "command": "ENTR"
                                "data" = {
                                    "code": 200,
                                    "message: "xxx",
                                    "room_name": "xxx",
                                    "player": {
                                        "user": {
                                            "username": "xx"
                                            "score": 10
                                        },
                                        "player_id": random_id,
                                        "direction": data["direction"],
                                        "pos": str(random_id) + ":" + data["pos"].split(":")[1]
                                    },
                                    "players": []
                                }
                            }
                            """
                            res_code    = rp["data"]["code"]
                            res_message = rp["data"]["message"]
                            room_name   = rp["data"]["room_name"]
                            player      = rp["data"]["player"]
                            players     = rp["data"]["players"]
                            if res_code == 200:
                                pid  = player["player_id"]
                                if self.player_id == None:
                                    self.player_id = pid
                                    self.active_room["players"] = players
                                    self.active_room["room_name"] = room_name
                                else:
                                    # Add Other Connected Players
                                    self.active_room["players"].append(player)
                            else: 
                                # Enter room request failed. Room full.
                                print(res_code, res_message, room_name)
                        if command == "LVER":
                            """
                            {
                                "command": "LVER"
                                "data" = {
                                    "player": {
                                        "user": {
                                            "username": "xx"
                                            "score": 10
                                        },
                                        "player_id": random_id,
                                        "direction": data["direction"],
                                        "pos": str(random_id) + ":" + data["pos"].split(":")[1]
                                    }
                                }
                            }
                            """
                            player = rp["data"]["player"]
                            self.active_room["players"].remove(player)
                            
                            pid   = player["player_id"]
                            for t in self.tank_group.sprites():
                                if t.tid == pid:
                                    t.kill()

                        if command == "SRTG":
                            # Start game signal from server
                            code = rp["data"]["code"]
                            ## players - [{'user': {'username': 'oguzhan', 'score': 10}, 'player_id': 3, 'direction': 'bottom', 'pos': '3:123,145'}]
                            if code == 200:
                                for player in self.active_room["players"]:
                                    player_id = player["player_id"]
                                    img  = ""
                                    if player_id == 0:
                                        img = "assets/tank_dark.png"
                                    elif player_id == 1:
                                        img = "assets/tank_green.png"
                                    elif player_id == 2:
                                        img = "assets/tank_sand.png"
                                    else:
                                        img = "assets/tank_blue.png"

                                    if player["player_id"] == self.player_id:
                                        self.tank.tid = player_id
                                        self.tank.direction = player["direction"]
                                        self.tank.change_img(img)
                                        self.tank_group.add(self.tank)
                                    else:
                                        x = player["pos"].split(":")[1].split(",")[0]
                                        y = player["pos"].split(":")[1].split(",")[1]
                                        self.tank_group.add(Tank(img, int(x), int(y), player_id, self))
                                        self.tank_group.add(Tank(img, int(x), int(y), player_id, self))
                                self.game_started = True

                        if command == "MOVE": 
                            """
                            {
                                "command": "MOVE", 
                                "data": {
                                    "player_id": 1,
                                    "direction": "bottom", 
                                    "pos": "1:121,111"
                                }
                            }
                            """
                            ############ Update Other Tank Positions #############
                            pid         = rp["data"]["player_id"]
                            direction   = rp["data"]["direction"]
                            centerx     = rp["data"]["pos"].split(":")[1].split(",")[0]
                            centery     = rp["data"]["pos"].split(":")[1].split(",")[1]
                            for t in self.tank_group.sprites():
                                if t.tid != self.player_id:
                                    if t.tid == pid:
                                        t.rect.centerx = int(centerx)
                                        t.rect.centery = int(centery)
                                        if t.direction != direction:
                                            if direction == "left":
                                                t.turn_left()
                                            elif direction == "right":
                                                t.turn_right()
                                            elif direction == "top":
                                                t.turn_up()
                                            elif direction == "bottom":
                                                t.turn_down()
                            #######################################################
                        if command == "SHOT":
                            ########### Add Other Tank Bullets To Screen ##########
                            pid   = rp["data"]["player_id"]
                            for t in self.tank_group.sprites():
                                if pid != self.player_id:
                                    if t.tid == pid:
                                        t.shoot()
                            #######################################################

                    except: # json errors
                        print("HEEYYY DATA:")
                        print(reply)
                        # it occurs when recv receives two command object in same packet like:
                        # "{'command': 'MOVE', 'data': {'player_id': 1, 'direction': 'bottom', 'pos': '1:301,204'}}{'command': 'MOVE', 'data': {'player_id': 1, 'direction': 'bottom', 'pos': '1:301,204'}}"
                        # E.g:  b'{"command": "STRT", "data": "hi server"}{"command": "TANK", "data": {"player_id": 1}}'
                        traceback.print_exc()
                        pass
            except Exception:
                traceback.print_exc()
                break

    def organize_string_data(self, data: str):
        if data.find("}{") != -1:
            i = data.find("}{")
            t = data.replace("}{", "}")
            return t[:i+1]
        return data
      