import socket
import RSA
import AES

from Models.Message import Message
from Communication import Communication

class Key_Swap:
    _privRSA, _publRSA = RSA.generate_rsa_keys()

    @staticmethod
    def swap_keys(soc):
        """
        doesan rsa encrypted key swap
        :param soc: socket of the the client
        :return: an aes key that the client sends
        """


        # Sending the RSA public key
        msg = Message(0x6969, 0x0001,Key_Swap._publRSA)
        msg_data = msg.prepare()
        Communication.send_with_size(soc, msg_data)

        aes_key_msg = Message.load_from_bdata(Communication.recv_by_size())
        if len(aes_key_msg.fields) >= 1 and aes_key_msg.status == 0x0003 and aes_key_msg.opcode == 0x6969:
            aes_key = RSA.decrypt_message(aes_key_msg[0], Key_Swap._privRSA)

            #in case of success
            msg = Message(0x6969, 0x0002, b"OK")
            msg_data = msg.prepare()
            Communication.send_with_size(soc, msg_data)

            return aes_key

        #in case of failure
        msg = Message(0x6969, 0x0002, b"FAIL")
        msg_data = msg.prepare()
        Communication.send_with_size(soc, msg_data)

        return None
