import socket
from Dependencies import KeySwap
from Thread import Thread
from Dependencies.Communication import Communication

def main(ip, port):
    server_socket = socket.socket()
    server_socket.bind((ip, port))
    server_socket.listen()
    print("server up and running")

    while True:
        (c_socket, c_address) = server_socket.accept()
        print("connection from:" + str(c_address))
        key = KeySwap.Key_Swap.swap_keys(c_socket)
        print(key)
        com = Communication(c_socket, key)
        t = Thread(com)
        t.start()


if __name__ == '__main__':
    main('127.0.0.1', 4133)
