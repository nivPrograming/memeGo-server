import socket
import struct

class Message:
    def __init__(self, opcode, status, *args):
        self.opcode = opcode
        self.status = status
        self.fields = args

    def prepare(self):
        data = struct.pack("H", socket.htons(self.opcode))
        data += struct.pack("H", socket.htons(self.status))
        for i in self.fields:
            arg_len = struct.pack("I", socket.htonl(len(i)))
            data += arg_len + i

        return data

    @staticmethod
    def load_from_bdata(bdata):
        if len(bdata) < 4:
            return None
        opcode = socket.ntohs(struct.unpack("H", bdata[0:2])[0])
        status = socket.ntohs(struct.unpack("H", bdata[2:4])[0])
        fields = []
        offset = 4
        while offset <= len(bdata) - 4:
            f_size = socket.ntohl(struct.unpack("I", bdata[offset:offset+4])[0])
            if offset+4+f_size <= len(bdata):
                fields.append(bdata[offset+4: offset+4+f_size])
                offset = offset+4+f_size
            else:
                return None

        return Message(opcode, status, *fields)





