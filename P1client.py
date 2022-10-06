import socket
HOST = 'localhost'
PORT = 8889 # Arbitrary non-privileged port

while True:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.settimeout(None)
    clientSocket.connect((HOST, PORT))
    inputFromKeyboard = input('Enter command: ') # get command from user
    clientSocket.send(inputFromKeyboard.encode()) # send command to server
    if (inputFromKeyboard=='exit'): # If input from user is 'exit', close connection
        break
    print ('waiting for response from server...')
    receivedMessage = clientSocket.recv(1024) # Get reply from server
    print ('server response received: ')
    print (receivedMessage.decode()) # Print the reply on the screen
    clientSocket.close()
