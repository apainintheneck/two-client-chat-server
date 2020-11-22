#Assignment #3 TCP Client-Server Extra Credit
#Program: TCP Client
#Group #6
#Members: Jeannie Davis, Kevin Robell, Harsandeep Singh
#Purpose: A chat client that communicates with another client through
#the server. You can send
from socket import *

#Purpose: Create socket and connect to another socket.
#Input: Host and port number of socket to connect to.
def createSock(host, port):
   sock = socket(AF_INET, SOCK_STREAM)
   sock.connect((host, port))
   return sock

#Purpose: Receive messages from chat partner.
#When '\0' is received, stop receiving.
#When 'Bye' is received, end chat.
def receive(sock, chatid):
   message = ''
   #Receive messages from server until '\0' or 'Bye' is received.
   while message.strip() != '\0':
      message = sock.recv(1024).decode()
      if message.strip() != '\0':
         print('Client ' + chatid + ': ' + message)
         #End chat if 'Bye' was received.
         if message.strip() == 'Bye':
            sock.send(b'End\0') #Alert server to close connection.
            return False
   return True

#Purpose: Send messages to chat partner.
#When '\0' is sent, stop sending.
#When 'Bye' is sent, end chat.
def send(sock):
   message = ''
   #Send messages to server until '\0' or 'Bye' is sent.
   while message.strip() != '\0':
      message = input('You: ')
      if message.strip() == '':
         message = '\0'
      sock.send(message.encode())
      #End chat if 'Bye' was sent.
      if message.strip() == 'Bye':
         return False
   return True

def main():
   clientSock = createSock('', 1200)
   serverMessage = clientSock.recv(1024).decode()
   print('From Server:', serverMessage)
   
   print('Tip #1: Enter a blank line to stop sending and start receiving.')
   print('Tip #2: Enter "Bye" to end chat.')
   print('---Chat---')

   #Record id of chat partner
   chatid = serverMessage.split()[-1]
   
   #Keep the chat open until 'Bye' is either sent or received.
   #In that case, receive() or send() will return False.
   while True:
      if not receive(clientSock, chatid):
         break
      if not send(clientSock):
         break

   print('Ending chat...')
   clientSock.close()

if __name__ == '__main__':
   main()
