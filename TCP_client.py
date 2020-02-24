from socket import * 
import select
import errno

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
        print('loop')
        modifiedMsg = cli_sock.recv(2048)
        print (modifiedMsg.decode('utf-8'))
    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        # We just did not receive anything
        continue
    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()
      


cli_sock.close()
