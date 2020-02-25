from socket import * 
import select
import errno,sys,os
from threading import Thread
import time
from signal import signal, SIGINT

#test
MAX_BUF = 2048
SERV_PORT = 50000

serv_sock_addr = ('127.0.0.1', SERV_PORT)
cli_sock = socket(AF_INET, SOCK_STREAM)
cli_sock.connect(serv_sock_addr)

def main():
  username = input('Enter your name: ')
  while True:
    txtout = input(f'{username}: ')
    if txtout == 'quit':
      break
    if txtout:
      inputMessage = txtout.encode('utf-8')
      message = txtout.split()
      if message[0] == 'publish':
        lenght = len(message)
        publish(inputMessage,lenght)
      elif message[0] == 'subscribe':
        try:
          cli_sock.send(inputMessage)
          Thread(target=subscribe, args=()).start()
        except:
          print("Cannot start thread..")
          import traceback
          trackback.print_exc()  
  cli_sock.close()
      
def publish(inputMessage,length):
  if length > 2:
    cli_sock.send(inputMessage)
    modifiedMsg = cli_sock.recv(2048)
    print (modifiedMsg.decode('utf-8'))

def subscribe():
  signal(SIGINT,handler)
  while True:
    modifiedMsg = cli_sock.recv(2048)
    print (modifiedMsg.decode('utf-8'))






# Handle Ctrl-C Interrupt
if __name__ == '__main__':
   try:
     main()
   except KeyboardInterrupt:
     print ('Interrupted ..')
     try:
       sys.exit(0)
     except SystemExit:
       os._exit(0)