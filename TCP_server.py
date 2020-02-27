from socket import * 
from threading import Thread
from collections import defaultdict
import os,sys
import time

dictSubscribe = defaultdict(list)
SERV_PORT = 50000

def handleClient(clientSocket,ip,port):
  while True:
    try:
      txtin = clientSocket.recv(1024)
      decodeTxt = txtin.decode('utf-8')
      if decodeTxt == '':
        clientSocket.close()
        print(f"\nclose connection ip: {ip}:{port}\n")
        break
      print (f'Client> {decodeTxt}') 
      command = decodeTxt.split()
      command[0] = command[0].lower()
      if txtin == b'quit':
          print(f'Client {ip}:{port} disconnected ...')
          break
      elif command[0] == 'subscribe' and len(command) >= 3:
          handleSubscribe(clientSocket,command[2])
      elif command[0] == 'publish' and len(command) >= 4:
          handlePublish(clientSocket,command[2],decodeTxt) 
      else:
        msg = "Don't have command"
        clientSocket.send(bytes(msg,"utf-8"))
    except:
      clientSocket.close()
      print(f"\nclient close connection ip: {ip}:{port}\n")
      break
  return

def handleSubscribe(subscribeSocket,topic):
  dictSubscribe[topic].append(subscribeSocket)
  msg = "You subscribe topic: " + topic
  subscribeSocket.send(bytes(msg,"utf-8"))

def handlePublish(publishSocket,topic,value):
  if dictSubscribe[topic]:
    count = 0
    continuePublish = True
    message = value.split(topic)
    while continuePublish:
      try:
        dictSubscribe[topic][count].send(bytes(message[1],"utf-8"))
        if count < len(dictSubscribe[topic])-1:
          count += 1
        else:
          continuePublish = False
      except:
        if count < len(dictSubscribe[topic])-1:
          count += 1
          continue
        else:
          continuePublish = False
    msg = f'publish topic: {topic} finished'
    publishSocket.send(bytes(msg,"utf-8"))
  else:
    msg = "Don't have subscriber"
    publishSocket.send(bytes(msg,'utf-8'))



def main():
  serv_sock_addr = ('127.0.0.1', SERV_PORT) #ประกาศเซิพไอพีอะไร
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
