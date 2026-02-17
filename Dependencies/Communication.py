import socket
from Dependencies import AES
import struct
from Models.Message import Message


class Communication:
    SIZE_HEADER_FORMAT = b"0000"  # n digits for data size + one delimiter
    size_header_size = len(SIZE_HEADER_FORMAT)
    TCP_DEBUG = False
    LEN_TO_PRINT = 100

    def __init__(self, soc, cipher_key):
        self.soc = soc
        self.key = cipher_key

    def send(self, msg):
        data = msg.prepare()

        enc_data = AES.aes_gcm_encrypt(data, self.key)
        print(f"Encrypted: {data} To: {enc_data}\nkey: {self.key}")

        self.send_with_size(self.soc, enc_data)

    def recv(self):
        data = self.recv_by_size(self.soc)
        if data != b'':
            print(data)
            dec_data = AES.aes_gcm_decrypt(data, self.key)

            data = Message.load_from_bdata(dec_data)
            print(f"DATA: {data.fields}")
            return data
        return None

    @staticmethod
    def recv_by_size(sock):
        size_header = b''
        data_len = 0
        while len(size_header) < Communication.size_header_size:
            _s = sock.recv(Communication.size_header_size - len(size_header))
            if _s == b'':
                size_header = b''
                break
            size_header += _s
        # Now, the size header field has entirely received in size_header (which is binary).
        data = b''
        if size_header != b"":
            data_len = socket.ntohl(struct.unpack("I", size_header)[0])
            while len(data) < data_len:
                _d = sock.recv(data_len - len(data))
                if _d is None:
                    data = b""
                    break
                data += _d

        if data_len != len(data):
            data = b""  # Partial data is like no data !
        return data

    @staticmethod
    def send_with_size(sock, bdata):
        len_data = len(bdata)
        header_data = struct.pack("I", socket.htonl(len(bdata)))
        if type(bdata) is not bytes:
            bdata = bdata.encode()
        bytea = header_data + bdata

        sock.send(bytea)

