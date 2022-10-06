from socket import *
import sys

class Node: # Customer Record Class
    def __init__(self,customerID, customerFirstName, customerLastName, customerPhone, customerAddress):
        self.id = customerID
        self.first = customerFirstName
        self.last = customerLastName
        self.phone = customerPhone
        self.address = customerAddress
    def display(self):  # display record
        return 'Customer record: ' + str(self.id) + ' ; ' + self.first + ' ; ' + self.last + ' ; ' + self.phone + ' ; ' + self.address

class customerDB: # Customer Database Class
    def __init__(self):
        self.db = []
    def showAll(self): # display all records
        allRecords = ''
        for record in self.db:
            allRecords = allRecords + record.display() + '\n'
        if (allRecords == ''):
            return 'Database is empty!'
        else:
            return allRecords

nextCustomerID = 0

cDB = customerDB()  # create customer database
#Fill in start                                                              
#Many lines of code to fill in here for other functions
#Fill in end  
def showAll():
    return cDB.showAll()
    
def show(ID):
    r_entry = Node('','','','','')
    for entry in cDB.db:
        if entry.id == int(ID):
            return entry.display()
    r_entry = 'Customer does not exist'
    return r_entry
    
def insert(ID, fname, lname, phone, address):
    customer = Node(nextCustomerID, fname, lname, phone, address)
    cDB.db.append(customer)

def remove(ID):
    for entry in cDB.db:
        if entry.id == int(ID):
            cDB.db.remove(entry)
            break
    return 'Customer not found'

def search(lname):
    for entry in cDB.db:
        if entry.last == str(lname):
            return entry.display()
    return 'Customer does not exist'

def change(id, fname, lname, phone, address):
    for entry in cDB.db:
        if entry.id == int(id):
            entry.first = fname
            entry.last = lname
            entry.phone = phone
            entry.address = address
            return 'Customer changed successfully'
    return 'Customer not found'

def dbupload(file):
    cDB.db.clear()
    newDB = open(file)
    newDBL = newDB.readlines()
    for item in newDBL:
        item2 = item.replace('Customer record: ', '')
        item3 = item2.replace('\n','')
        customer = item3.split(' ; ')
        custN = Node(int(customer[0]), customer[1], customer[2], customer[3], customer[4])
        cDB.db.append(custN)
    newDB.close()
    return 'New database uploaded successfully'

def dbdownload(file):
    DBFile = open(file, 'w')
    for item in cDB.db:
        DBFile.write(item.display() + '\n')
    DBFile.close()
    return 'Database downloaded successfully'
        
        
#Fill in start                                                              
# Many lines of code to fill in here
#Fill in end

serverPort = 8889
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ('The server is ready to receive...')
while True:
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024)
    function = message.decode().split()
    match function[0]:
        case 'showAll':
            response = showAll()
        case 'show':
            response = show(function[1])
        case 'insert':
            nextCustomerID+=1
            insert(nextCustomerID, function[1], function[2], function[3], function[4])
            response = 'Success'
        case 'exit':
            break
        case 'remove':
            remove(function[1])
            response = 'Customer removed'
        case 'search':
            response = search(function[1])
        case 'change':
            response = change(function[1], function[2], function[3], function[4], function[5])
        case 'dbdownload':
            response = dbdownload(function[1])
        case 'dbupload':
            response = dbupload(function[1])
        case _:
            response = 'No action taken'
    connectionSocket.sendall(response.encode())
    connectionSocket.close()
