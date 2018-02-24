import os
import sys
import socket
import pickle
import threading
from PySide import QtGui, QtCore

class Window(QtGui.QWidget):

    def __init__(this):
        super(Window, this).__init__()
        this.initUI()



    def initUI(this):
        this.setGeometry(300, 300, 250, 150)
        this.setWindowTitle('Icon')
        this.setWindowIcon(QtGui.QIcon('archlinux-512'))
        this.close_button = QtGui.QPushButton(this)
        this.close_button.setGeometry(QtCore.QRect(0, 0, 100, 50))
        this.close_button.clicked.connect(exit)
        this.close_button.setText("Close Server")
        this.show()
def clientthread(client_socket,client_address):
    while True:
        try:
            data = pickle.loads(client_socket.recv(4096))
            if isinstance(data, list):
                if len(data) == 2:
                    if data[0] == "showDir":
                        root, dirs, files = next(os.walk(data[1]))
                        send = []
                        send.append(File(".."))
                        for x in dirs:
                            send.append(Directory(x, []))
                        for x in files:
                            send.append(File(x))
                        client_socket.sendall(pickle.dumps(send))
                    elif data[0] == "mkDir":
                        os.makedirs(data[1])
                        data[1] = data[1][:data[1].rfind("/")]
                        data[1] = data[1][:data[1].rfind("/")+1]
                        root, dirs, files = next(os.walk(data[1]))
                        send = []
                        send.append(File(".."))
                        for x in dirs:
                            send.append(Directory(x, []))
                        for x in files:
                            send.append(File(x))
                        client_socket.sendall(pickle.dumps(send))
                    else:
                        if check_credentials(data):
                            client_socket.sendall("login_successful")
                        else:
                            client_socket.sendall("login_unsuccessful")

                else:
                    validity = register(data)
                    if validity[0] == "":
                        client_socket.sendall("s")
                        os.makedirs("./users/" + validity[1])
                    else:
                        client_socket.sendall(validity[0])

        except:
            print str(client_address[0]) + ":" + str(client_address[1]) + " has disconnected."
            client_socket.close()
            break
class User(object):
    def __init__(this, username, email, password):
        this.username = username
        this.email = email
        this.password = password
def check_credentials(data):
    for x in users:
        if x.username == data[0] and x.password == data[1]:
            return True
    return False
def register(data):
    ret = []
    ret.append("")
    username_valid = True
    email_valid = True
    password_valid = True
    for x in users:
        if data[0] == x.username:
            username_valid = False
        if data[1] == x.email:
            email_valid = False
        if not username_valid and not email_valid:
            break
    if len(data[2]) <= 5:
        password_valid = False
    if not username_valid: ret[0]+="u"
    if not email_valid: ret[0]+="e"
    if not password_valid: ret[0]+="p"
    if username_valid and email_valid and password_valid:
        users.append(User(data[0], data[1], data[2]))
        ret.append(data[0])
        ret.append(data[1])
        ret.append(data[2])
    return ret
class File(object):
    def __init__(this, fileName):
        this.fileName = fileName
class Directory(object):
    def __init__(this, dirName, files):
        this.dirName = dirName
        this.files = files
def exit():
    print "writing users..."
    data = ""
    for x in users:
        data += x.username + " "
        data += x.email + " "
        data += x.password + "\n"
    with open('database.txt', 'w+') as file:
        file.write(data)
    global clients
    for x in clients:
        x[0].close()
    server_socket.close()
    sys.exit()
    os._exit(0)
def acceptClients():
    global index
    global clients
    clients = []
    while True:
        (client_socket, client_address) = server_socket.accept()
        clients.append((client_socket, client_address))
        print str(client_address[0]) + ":" + str(client_address[1]) + " has connected."
        t = threading.Thread(target=clientthread, args=(client_socket, client_address))
        client_threads.append(t)
        client_threads[index].daemon = True
        client_threads[index].start()
        index += 1
users = []
if os.path.exists("database.txt"):
    exists = True
    with open('database.txt', 'r') as file:
        data = file.readlines()
    for x in data:
        if x != "\n":
            username, email, password = x.split()
            users.append(User(username, email, password))
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8820))
server_socket.listen(3)
print "Server has started. to close type exit."
client_threads = []
global index
index = 0
t1 = threading.Thread(target=acceptClients)
t1.daemon = True
t1.start()
a = QtGui.QApplication(sys.argv)
w = Window()
a.exec_()


