from socket import * 
from threading import Thread
from collections import defaultdict
import os,sys

dictSubscribe = defaultdict(list)
delClientConect = defaultdict(list)
SERV_PORT = 50000

def handleClient(clientSocket,ip,port):
  while True:
      txtin = clientSocket.recv(1024)
      # if not len(txtin):
      #    delDict(clientSocket)
      #    break
      decodeTxt = txtin.decode('utf-8')
      print (f'Client> {decodeTxt}') 
      command = decodeTxt.split()
      if txtin == b'quit':
          print(f'Client {ip}:{port} disconnected ...')
          break
      elif command[0] == 'subscribe' and len(command) >= 3:
          handleSubscribe(clientSocket,command[2])
      elif command[0] == 'publish' and len(command) >= 3:
          handlePublish(clientSocket,command[2],command[3]) 
      else:
          msg = "Don't have command"
          clientSocket.send(bytes(msg,"utf-8"))

def handleSubscribe(subscribeSocket,topic):
  dictSubscribe[topic].append(subscribeSocket)
  position = len(dictSubscribe[topic])-1
  delClientConect[socket].append(position)
  delClientConect[socket].append(topic)
  msg = "You subscribe topic: " + topic
  subscribeSocket.send(bytes(msg,"utf-8"))

def handlePublish(publishSocket,topic,value):
  if dictSubscribe[topic]:
    count = 0
    continuePublish = True
    while continuePublish:
      dictSubscribe[topic][count].send(bytes(value,"utf-8"))
      if count < len(dictSubscribe[topic])-1:
        count += 1
      else:
        continuePublish = False
  else:
    msg = "Don't have subscriber"
    publishSocket.send(bytes(msg,'utf-8'))
  
def delDict(socket):
  position = dictSubscribe[socket][0]
  topic = dictSubscribe[socket][1]
  del dictSubscribe[topic][position]
  del delClientConect[socket]
  socket.shutdown(SHUT_RDWR)

def main():
  serv_sock_addr = ('127.0.0.1', SERV_PORT)
  welcome_sock = socket(AF_INET, SOCK_STREAM) #use TCP
  welcome_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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

  conn_sock.close()

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
