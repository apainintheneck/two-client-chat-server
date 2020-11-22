#Assignment #3 TCP Client-Server Extra Credit
#Program: TCP Server
#Group #6
#Members: Jeannie Davis, Kevin Robell, Harsandeep Singh
#Purpose: A chat server that pipes messages between two clients.
from socket import *
import threading

#Purpose: Create server socket and start listening.
def createSock(host, port):
   sock = socket(AF_INET, SOCK_STREAM)
   sock.bind((host, port))
   sock.listen()
   return sock

#Purpose: A pipe that redirects messages from inSock to outSock.
def sockPipe(inSock, outSock):
   message = ''
   #Pipe messages until a message contains 'Bye' or 'End\0'
   while message.strip() != 'Bye':
      #Receive message from client.
      message = inSock.recv(1024).decode()
      #If receive 'End\0', close the pipe.
      if message.strip() == 'End\0':
         break
      #Send message to client
      outSock.send(message.encode())

def main():
   serverSock = createSock('', 1200)
   print('The chat server is waiting to receive 2 connections....\n')

   #Accept first client connection.
   connSock1, addr = serverSock.accept()
   print('Accepted first connection')

   #Accept second client connection.
   connSock2, addr = serverSock.accept()
   print('Accepted second connection')

   #Send connection messages to both clients
   connSock1.send(b'Connected to client Y', )
   connSock2.send(b'Connected to client X')

   #Create threads
   thread1 = threading.Thread(target=sockPipe, args=(connSock1, connSock2))
   thread2 = threading.Thread(target=sockPipe, args=(connSock2, connSock1))

   #Start threads
   thread1.start()
   thread2.start()
   
   #Send '\0' to switch one connection socket to sending.
   connSock1.send(b'\0')

   #Bind threads
   thread1.join()
   thread2.join()

   #Close connections
   connSock1.close()
   connSock2.close()

   print('\nClosing connections and shutting down chat server.')

if __name__ == '__main__':
   main()
