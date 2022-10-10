import socket
HOST = 'localhost'
PORT = 8889  # Arbitrary non-privileged port

while True:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.settimeout(None)
    clientSocket.connect((HOST, PORT))
    inputFromKeyboard = input('Enter command: ')  # get command from user
    if (inputFromKeyboard == 'dbupload'):
        dbU = open('filename.txt')
        dbUL = dbU.readlines()
        dbUL.insert(0, 'dbupload ')
        dbU.close()
        message = "".join(dbUL)
    else:
        message = inputFromKeyboard

    clientSocket.send(str(len(message)).encode())

    clientSocket.sendall(message.encode())  # send command to server
    if (inputFromKeyboard == 'exit'):  # If input from user is 'exit', close connection
        break

    #print ('waiting for response from server...')
    msgLen = int(clientSocket.recv(1024).decode())
    msgRecv = 0
    fragment = []
    while msgRecv < msgLen:
        chunk = clientSocket.recv(1024).decode()
        fragment.append(chunk)
        msgRecv += len(chunk)
    receivedMessage = "".join(fragment)
    if 'dbdownload' in receivedMessage:
        splitMessage = receivedMessage.split('\n')
        splitMessage.pop(0)
        dbD = open('filename.txt', 'w')
        for item in splitMessage:
            dbD.write(item + '\n')
        dbD.close()
        print('Operation was completed successfully.')
    else:
        #print ('server response received: ')
        print(receivedMessage)  # Print the reply on the screen
    clientSocket.close()
