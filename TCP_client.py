from socket import * 
import select
import errno,sys,os
from threading import Thread

MAX_BUF = 2048
SERV_PORT = 50000
getInput = True
username = ''

def main():
    username = input('Enter your name: ')
    while True:
        if getInput:
            message = input(f'{username} > ')
            if message:
                messageCut = message.split()
                if len(messageCut) >= 3:
                    socket = connection(message,messageCut[1])
                    messageCut[0] = messageCut[0].lower()
                    if socket:
                        if messageCut[0] == 'subscribe': 
                            Thread(target=subscribeMessage, args=(message, socket)).start()
                        elif messageCut[0] == 'publish':
                            publishMessage(message,socket)
                        else:
                            print("\nDon't have command\n")
                elif messageCut[0] == 'quit' and len(messageCut) == 1:
                    print('exit program')
                    break
                else:
                    print("\nDon't have command\n")
            continue

def connection(message,ip):
    serv_sock_addr = (ip, SERV_PORT)
    cli_sock = socket(AF_INET, SOCK_STREAM)
    try:
        cli_sock.connect(serv_sock_addr)
        return cli_sock
    except:
        print(f"connection error ip: {ip}")
        return False

def subscribeMessage(message,socket):
    global getInput
    getInput = False
    socket.send(bytes(message,"utf-8"))
    while True:
        try:
            msgServer = socket.recv(2048)
            print(msgServer.decode('utf-8'))
        except:
            print('server close connection')
            socket.close()
            break
    getInput = True


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