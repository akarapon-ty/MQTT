from socket import * 
import select
import errno
import time

#test
MAX_BUF = 2048
SERV_PORT = 50000

serv_sock_addr = ('127.0.0.1', SERV_PORT)
cli_sock = socket(AF_INET, SOCK_STREAM)
cli_sock.connect(serv_sock_addr)
cli_sock.setblocking(False)

username = input('Enter your name: ')
while True:
    txtout = input(f'{username}: ')
    if txtout:
      message = txtout.encode('utf-8')
      cli_sock.send(message)
    if txtout == 'quit':
      break
    try:
      while True:
        time.sleep(0.2)
        modifiedMsg = cli_sock.recv(2048)
        print (modifiedMsg.decode('utf-8'))
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue
    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()
      


cli_sock.close()
