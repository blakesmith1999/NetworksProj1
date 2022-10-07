import socket
HOST = 'localhost'
PORT = 8889 # Arbitrary non-privileged port

while True:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.settimeout(None)
    clientSocket.connect((HOST, PORT))
    inputFromKeyboard = input('Enter command: ') # get command from user
    if (inputFromKeyboard == 'dbupload'):
        dbU = open('filename.txt')
        dbUL = dbU.readlines()
        dbUL.insert('dbupload', 0)
        message = dbUL
    else:
        message = inputFromKeyboard

    clientSocket.sendall(message.encode()) # send command to server
    if (inputFromKeyboard=='exit'): # If input from user is 'exit', close connection
        break

    #print ('waiting for response from server...')
    fragment = []
    while True:
        chunk = clientSocket.recv(1024)
        if not chunk:
            break
        fragment.append(chunk.decode())
    receivedMessage = "".join(fragment)
    #print ('server response received: ')
    print (receivedMessage) # Print the reply on the screen
    clientSocket.close()
