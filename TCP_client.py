from socket import * 
import select
import errno
import time,sys

#test
MAX_BUF = 2048
SERV_PORT = 50000

serv_sock_addr = ('127.0.0.1', SERV_PORT)
cli_sock = socket(AF_INET, SOCK_STREAM)
cli_sock.connect(serv_sock_addr)
cli_sock.setblocking(False)
loop = True

username = input('Enter your name: ')
while True:
    txtout = input(f'{username}: ')
    if txtout:
      message = txtout.encode('utf-8')
      cli_sock.send(message)
    if txtout == 'quit':
      loop = False
      break
    # elif message[0] == 'publish':
    #   loop = False
    #   response = cli_sock.recv(2048)
    #   print (response.decode('utf-8'))
    # elif message[0] == 'subscribe':
    #   loop = True
    while True:
      try:
          modifiedMsg = cli_sock.recv(2048)
          if modifiedMsg:
            print (modifiedMsg.decode('utf-8'))
            break
      except Exception as e:
          print('Reading error: '.format(str(e)))
          sys.exit()

cli_sock.shutdown(SHUT_RDWR)



