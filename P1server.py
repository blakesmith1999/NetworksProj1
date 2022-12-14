from ast import arg
from socket import *


class Node:  # Customer Record Class
    def __init__(self, customerID, customerFirstName, customerLastName, customerPhone, customerAddress):
        self.id = customerID
        self.first = customerFirstName
        self.last = customerLastName
        self.phone = customerPhone
        self.address = customerAddress

    def display(self):  # display record
        return 'Customer record: ' + str(self.id) + ' ; ' + self.first + ' ; ' + self.last + ' ; ' + self.phone + ' ; ' + self.address + '\n'


class customerDB:  # Customer Database Class
    def __init__(self):
        self.db = []

    def showAll(self):  # display all records
        allRecords = ''
        for record in self.db:
            allRecords = allRecords + record.display()
        if (allRecords == ''):
            return 'Database is empty!'
        else:
            return allRecords


nextCustomerID = 0

cDB = customerDB()  # create customer database
#Fill in start
# Many lines of code to fill in here for other functions
#Fill in end


def showAll():
    return cDB.showAll()


def show(function):
    for entry in cDB.db:
        if entry.id == int(function[1]):
            return entry.display()
    return 'ERROR: No match was found!'


def insert(ID, function):
    customer = Node(ID, function[1], function[2], function[3], function[4])
    cDB.db.append(customer)
    return 'Operation was completed successfully.'


def remove(function):
    for entry in cDB.db:
        if entry.id == int(function[1]):
            cDB.db.remove(entry)
            return 'Operation was completed successfully.'
    return 'ERROR: No match was found!'


def search(function):
    for entry in cDB.db:
        if entry.last == str(function[1]):
            return entry.display()
    return 'ERROR: No match was found!'


def change(function):
    for entry in cDB.db:
        if entry.id == int(function[1]):
            entry.first = function[2]
            entry.last = function[3]
            entry.phone = function[4]
            entry.address = function[5]
            return 'Operation was completed successfully.'
    return 'ERROR: No match was found!'


def dbupload(function):
    # we get function here as a list with each word separately, no spaces. Need to reassemble each customer by line
    # function.pop()
    database = " ".join(function)
    DL = database.split('Customer record: ')
    cDB.db.clear()
    for item in DL:
        if item != '':
            customer = item.split(' ; ')
            custN = Node(int(customer[0]), customer[1],
                         customer[2], customer[3], customer[4])
            cDB.db.append(custN)
    return 'Operation was completed successfully.'


def dbdownload():
    dbRet = ['dbdownload\n']
    for item in cDB.db:
        dbRet.append(item.display())
    return "".join(dbRet)

    # DBFile = open(function[1], 'w')
    # for item in cDB.db:
    #     DBFile.write(item.display() + '\n')
    # DBFile.close()
    # return 'Operation was completed successfully.'


def argnum_error(code):
    message = 'This command takes {} arguments. Check argument list and try again.'
    return message.format(str(code))

#Fill in start
# Many lines of code to fill in here
#Fill in end


serverPort = 8889
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive...')
while True:
    connectionSocket, addr = serverSocket.accept()
    msgLen = int(connectionSocket.recv(1024).decode())
    msgRecv = 0
    fragment = []
    while msgRecv < msgLen:
        chunk = connectionSocket.recv(1024).decode()
        fragment.append(chunk)
        msgRecv += len(chunk)
    receivedMessage = "".join(fragment)
    function = receivedMessage.split()
    if len(function) == 0:
        function.append('')
    match function[0]:
        case 'showAll':
            if len(function) == 1:
                response = showAll()
            else:
                response = argnum_error(0)
        case 'show':
            if len(function) == 2:
                response = show(function)
            else:
                response = argnum_error(1)
        case 'insert':
            if len(function) == 5:
                nextCustomerID += 1
                response = insert(nextCustomerID, function)
            else:
                response = argnum_error(4)
        case 'remove':
            if len(function) == 2:
                response = remove(function)
            else:
                response = argnum_error(1)
        case 'search':
            if len(function) == 2:
                response = search(function)
            else:
                response = argnum_error(1)
        case 'change':
            if len(function) == 6:
                response = change(function)
            else:
                response = argnum_error(5)
        case 'dbdownload':
            if len(function) == 1:
                response = dbdownload()
            else:
                response = argnum_error(0)
        case 'dbupload':
            # this is going to take significantly more work...
            response = dbupload(function[1:])
        case 'exit':
            break
        case _:
            response = 'ERROR: The operation is not supported!'

    connectionSocket.send(str(len(response)).encode())
    connectionSocket.sendall(response.encode())
    connectionSocket.close()
