import struct
import threading
from Dependencies.Communication import Communication
from Models.Message import Message
from Dependencies.CreatureManager import CreatureManager
from Dependencies.JWTHelper import JWTHelper


class Thread(threading.Thread):
    def __init__(self, com: Communication):
        super().__init__()
        self.com = com
        self.keepAlive = True
        self.cm = None
        self.last_location = (None, None)
        self.usr = None

    def run(self):
        self.cm = CreatureManager()

        while self.keepAlive:
            msg = self.com.recv()
            if msg is None:
                self.keepAlive = False

            else:
                match msg.opcode:
                    case 0x0001:  # Handling a request for a json web token
                        if msg.status == 0x0000 and len(msg.fields) >= 2:
                            email = None
                            psw = None
                            try:
                                email = msg.fields[0].decode()
                                psw = msg.fields[1].decode()
                            except (UnicodeDecodeError, AttributeError) as e:
                                reply = Message(0x0001, 0x0002)
                                self.com.send(reply)

                            else:
                                usr = self.cm.db.login_usr_psw(email, psw)
                                if usr == -1 or usr == -2:
                                    reply = Message(0x0001, 0x0002)
                                    self.com.send(reply)
                                else:
                                    self.usr = usr
                                    new_token = JWTHelper.create_token(usr.Email)
                                    reply = Message(0x0001, 0x0001, new_token.encode())
                                    self.com.send(reply)
                        else:
                            self.keepAlive = False

                    case 0x0002:  # Handling a new user signup
                        if msg.status == 0x0000 and len(msg.fields) >= 3:
                            email = None
                            psw = None
                            username = None
                            try:
                                email = msg.fields[0].decode()
                                psw = msg.fields[1].decode()
                                username = msg.fields[2].decode()
                            except (UnicodeDecodeError, AttributeError) as e:
                                reply = Message(0x0002, 0x0002)
                                self.com.send(reply)

                            else:
                                if not self.cm.db.insert_new_user(email, username, psw):
                                    reply = Message(0x0002, 0x0003)
                                    self.com.send(reply)
                                else:
                                    reply = Message(0x0002, 0x0001)
                                    self.com.send(reply)

                        else:
                            self.keepAlive = False


                    case 0x0007:  # Handling a player request for the creatures around him
                        if msg.status == 0x0000 and len(msg.fields) >= 2:
                            lat = struct.unpack("!d", msg.fields[0])[0]
                            lon = struct.unpack("!d", msg.fields[1])[0]
                            self.last_location = (lat, lon)
                            creatures = self.cm.find_creatures_around(lat, lon, 600)

                            if len(creatures) == 0:
                                self.com.send(Message(0x0007, 0x0002))

                            else:
                                c_fields = [c.to_bytes() for c in creatures]
                                reply = Message(0x0007, 0x0001, *c_fields)
                                self.com.send(reply)
                        else:
                            self.keepAlive = False

                    case 0x000B:  # Handling jwt log in
                        if msg.status == 0x0000 and len(msg.fields) >= 1:
                            token = None
                            try:
                                token = msg.fields[0].decode()
                            except (UnicodeDecodeError, AttributeError) as e:
                                reply = Message(0x000B, 0x0002)
                                self.com.send(reply)
                            else:
                                usr = self.cm.db.login_usr_jwt(token)
                                if usr == -1 or usr == -2:
                                    reply = Message(0x000B, 0x0002)
                                    self.com.send(reply)
                                else:
                                    self.usr = usr
                                    reply = Message(0x000B, 0x0001, usr.Username.encode())
                                    self.com.send(reply)
                        else:
                            self.keepAlive = False

                    case 0x000C:  # Handling normal email and psw login
                        if msg.status == 0x0000 and len(msg.fields) >= 2:
                            email = None
                            psw = None
                            try:
                                email = msg.fields[0].decode()
                                psw = msg.fields[1].decode()
                            except (UnicodeDecodeError, AttributeError) as e:
                                reply = Message(0x000C, 0x0002)
                                self.com.send(reply)

                            else:
                                usr = self.cm.db.login_usr_psw(email, psw)
                                if usr == -1 or usr == -2:
                                    reply = Message(0x000C, 0x0002)
                                    self.com.send(reply)
                                else:
                                    self.usr = usr
                                    reply = Message(0x000C, 0x0001, usr.Username.encode)
                                    self.com.send(reply)
                        else:
                            self.keepAlive = False

                    case _:
                        self.keepAlive = False

        self.com.soc.close()


