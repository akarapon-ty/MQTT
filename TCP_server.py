from socket import * 
from threading import Thread
import os,sys

SERV_PORT = 50000

def handleClient(s,ip,port):
  while True:
     txtin = s.recv(1024)
     decodeTxt = txtin.decode('utf-8')
     print ('Client> %s' %(txtin).decode('utf-8')) 
     print ('\n %s , %s' %(ip,port))
     command = decodeTxt.split()
     print('post: %s' %(command))
     if txtin == b'quit':
        print('Client disconnected ...')
        break
     elif command[0] == 'subscribe':
        #Thread(target=, args=(s,ip,port)).start()
        print('sd')
     else:
        txtout = txtin.upper()    
        s.send(txtout)
  s.close()
  return

#  def handleSubscribe(s,ip,port):
#      while True:
#          command = inputCommand.recv(1024)


def main():
  serv_sock_addr = ('10.35.250.190', SERV_PORT)
  welcome_sock = socket(AF_INET, SOCK_STREAM) #use TCP
  welcome_sock.bind(serv_sock_addr) 
  welcome_sock.listen(5)
  print ('TCP threaded server started ...')

  while True:
    conn_sock, cli_sock_addr = welcome_sock.accept()
    ip, port = str(cli_sock_addr[0]), str(cli_sock_addr[1]) 
    print ('New client connected from .. ' + ip + ':' + port)

    try:
      Thread(target=handleClient, args=(conn_sock, ip,port)).start()
    except:
      print("Cannot start thread..")
      import traceback
      trackback.print_exc()

  s.close()

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
