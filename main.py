import socket
from Dependencies import KeySwap
from Thread import Thread
from Dependencies.Communication import Communication
from GeneratorThread import GeneratorThread


def main(ip, port):

    server_socket = socket.socket()
    server_socket.bind((ip, port))
    server_socket.listen()
    print("server up and running")

    gen_t = GeneratorThread()
    gen_t.start()
    while True:
        (c_socket, c_address) = server_socket.accept()
        print("connection from:" + str(c_address))
        key = KeySwap.Key_Swap.swap_keys(c_socket)
        print(key)
        com = Communication(c_socket, key)
        t = Thread(com)
        gen_t.lock.acquire()
        gen_t.threads.append(t)
        gen_t.lock.release()
        t.start()


if __name__ == '__main__':
    main('127.0.0.1', 4133)
