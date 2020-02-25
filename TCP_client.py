from socket import * 
import select
import errno,sys,os
from signal import signal, SIGINT

MAX_BUF = 2048
SERV_PORT = 50000

username = ''

def main():
    username = input('Enter your name: ')
    while True:
        message = input(f'{username} > ')
        if message:
            messageCut = message.split()
            if len(messageCut) >= 3:
                socket = connection(message,messageCut[1])
                if messageCut[0] == 'subscribe':
                    if socket:
                        try:
                            subscribeMessage(message,socket)
                        except KeyboardInterrupt: 
                            print("\n Interrupted key")
                elif messageCut[0] == 'publish':
                    if socket:
                        publishMessage(message,socket)
            else:
                print("Don't have command")
        continue

def connection(message,ip):
    try: 
        socket.close()
    except:
        serv_sock_addr = (ip, SERV_PORT)
        cli_sock = socket(AF_INET, SOCK_STREAM)
        try:
            cli_sock.connect(serv_sock_addr)
            return cli_sock
        except:
            print(f"connection error ip: {ip}")
            return False

def subscribeMessage(message,socket):
    socket.send(bytes(message,"utf-8"))
    while True:
        try:
            msgServer = socket.recv(2048)
            print(msgServer.decode('utf-8'))
        except KeyboardInterrupt:
            print('Interrupt!!!')
        except:
            print('server close connection')
            socket.close()
            break


def publishMessage(message,socket):
    try:
        socket.send(bytes(message,"utf-8"))
        msgServer = socket.recv(2048)
        print(msgServer.decode('utf-8'))
    except:
        print('server close connection')
        socket.close()

# Handle Ctrl-C Interrupt
if __name__ == '__main__':
   try:
     main()
   except KeyboardInterrupt:
     print ('\nInterrupted ..')
     try:
       sys.exit(0)
     except SystemExit:
       os._exit(0)