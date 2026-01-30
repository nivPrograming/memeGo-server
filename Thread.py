import struct
import threading
from Dependencies.Communication import Communication
from Models.Message import Message
from Dependencies.CreatureManager import CreatureManager


class Thread(threading.Thread):
    def __init__(self, com: Communication):
        super().__init__()
        self.com = com
        self.keepAlive = True
        self.cm = None
        self.last_location = (None, None)

    def run(self):
        self.cm = CreatureManager()

        while self.keepAlive:
            msg = self.com.recv()
            if msg is None:
                self.keepAlive = False

            else:
                match msg.opcode:
                    case 0x0007:
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
                            reply = Message(0x0007, 0xFFFF)
                            self.com.send(reply)

                    case _:
                        self.keepAlive = False

        self.com.soc.close()


