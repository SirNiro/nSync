import os
import sys
import socket
import pickle
import threading
import shutil
os.system('pip install pyside')
from PySide import QtGui, QtCore
import uuid, smtplib
import time
uuid_dict = {}
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


def expiry(user, code):
    time.sleep(300)  # 5 minutes
    try:
        uuid_dict[user.username].remove(code)
    except:
        pass


def clientthread(client_socket,client_address):
    while True:
        try:
            data = client_socket.recv(4096)
        except:
            print str(client_address[0]) + ":" + str(client_address[1]) + " has disconnected."
            client_socket.close()
            break
        if not data:
            print str(client_address[0]) + ":" + str(client_address[1]) + " has disconnected."
            client_socket.close()
            break
        try:
            pickledata = pickle.loads(data)
            data = pickledata
        except:
            pass
        if isinstance(data, list):
                if data[0] == "showDir":
                    try:
                        root, dirs, files = next(os.walk(data[1]))
                        send = []
                        send.append(File(".."))
                        for x in dirs:
                            send.append(Directory(x))
                        for x in files:
                            send.append(File(x))
                        client_socket.sendall(pickle.dumps(send))
                    except:
                        print "fuck"
                        client_socket.sendall(pickle.dumps("doesn't exist"))
                elif data[0] == "mkdir":
                    try:
                        os.makedirs(data[1])
                        data[1] = data[1][:data[1].rfind("/")]
                        data[1] = data[1][:data[1].rfind("/")+1]
                        root, dirs, files = next(os.walk(data[1]))
                        send = []
                        send.append(File(".."))
                        for x in dirs:
                            send.append(Directory(x))
                        for x in files:
                            send.append(File(x))
                        client_socket.sendall(pickle.dumps(send))
                    except WindowsError:
                        client_socket.sendall(pickle.dumps("already exists"))
                elif data[0] == "rmdir":
                    try:
                        shutil.rmtree(data[1])
                        data[1] = data[1][:data[1].rfind("/")]
                        data[1] = data[1][:data[1].rfind("/")+1]
                        root, dirs, files = next(os.walk(data[1]))
                        send = []
                        send.append(File(".."))
                        for x in dirs:
                            send.append(Directory(x))
                        for x in files:
                            send.append(File(x))
                        client_socket.sendall(pickle.dumps(send))
                    except WindowsError:
                        client_socket.sendall(pickle.dumps("doesn't exist"))
                elif data[0] == "rm":
                    try:
                        os.remove(data[1])
                        data[1] = data[1][:data[1].rfind("/")]+"/"
                        root, dirs, files = next(os.walk(data[1]))
                        send = []
                        send.append(File(".."))
                        for x in dirs:
                            send.append(Directory(x))
                        for x in files:
                            send.append(File(x))
                        client_socket.sendall(pickle.dumps(send))
                    except WindowsError:
                        client_socket.sendall(pickle.dumps("doesn't exist"))
                elif data[0] == "mv":
                    try:
                        os.rename(data[1], data[2])
                        data[2] = data[2][:data[2].rfind("/")]
                        root, dirs, files = next(os.walk(data[2]))
                        send = []
                        send.append(File(".."))
                        for x in dirs:
                            send.append(Directory(x))
                        for x in files:
                            send.append(File(x))
                        client_socket.sendall(pickle.dumps(send))
                    except WindowsError:
                        client_socket.sendall(pickle.dumps("already exists"))
                elif data[0] == "login":
                    if check_credentials(data):
                        client_socket.sendall("login_successful")
                    else:
                        client_socket.sendall("login_unsuccessful")
                elif data[0] == "forgot_password1":
                    for x in users:
                        if x.username == data[1]:
                            client_socket.sendall("ok")
                            random = str(uuid.uuid4())[:6].upper()
                            if x.username in uuid_dict:
                                uuid_dict[x.username].append(random)
                            else:
                                uuid_dict[x.username] = [random]
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.ehlo()
                            server.starttls()
                            server.login("nsyncmail1@gmail.com", "cP6uY8a9")
                            msg = "\n".join([
                                "From: nsyncmail1@gmail.com",
                                "To: " + x.email,
                                "Subject: Password Reset",
                                "",
                                "Your reset code is: " + random +"\nYour code expires in 5 minutes."
                            ])
                            server.sendmail("nsyncmail1@gmail.com", x.email, msg)
                            server.quit()
                            t2 = threading.Thread(target=expiry, args=(x,random,))
                            t2.daemon = True
                            t2.start()
                            break
                    else:
                        client_socket.sendall("not ok")
                elif data[0] == "forgot_password2":
                    try:
                        for x in uuid_dict[data[1]]:
                            if x == data[2]:
                                client_socket.sendall("valid")
                                break
                        else:
                            client_socket.sendall("invalid")
                    except:
                        client_socket.sendall("invalid")
                elif data[0] == "forgot_password3":
                    if len(data[2]) > 5:
                        for x in users:
                            if x.username == data[1]:
                                x.password = data[2]
                                f = open("database.txt", "r")
                                lines = f.readlines()
                                f.close()
                                count = 0
                                for line in lines:
                                    l1, l2, l3 = line.split()
                                    if l1 == data[1]:
                                        lines[count] = x.username + " " + x.email + " " + x.password
                                        try:
                                            lines[count+1] = "\n" + lines[count+1]
                                        except:
                                            pass
                                        break
                                    count+=1
                                f = open("database.txt", "w")
                                for line in lines:
                                    f.write(line)
                                f.close()
                                uuid_dict[x.username].remove(data[3])
                                client_socket.sendall("changed")
                                break
                    else:
                        client_socket.sendall("invalid")
                elif data[0] == "register":
                    validity = register(data)
                    if validity[0] == "":
                        client_socket.sendall("s")
                        if os.path.exists("database.txt"):
                            f = open('database.txt', 'r')
                            text = f.read()
                            f.close()
                            f = open('database.txt', 'a')
                            if text == "":
                                f.write(data[1] + " " + data[2] + " " + data[3])
                            else:
                                f.write("\n"+ data[1] + " " + data[2] + " " + data[3])
                            f.close()
                        else:
                            f = open('database.txt', 'w')
                            f.write(data[1] + " " + data[2] + " " + data[3])
                            f.close()
                        if not os.path.isdir('users'):
                            os.mkdir('users')
                        os.makedirs("./users/" + validity[1])
                    else:
                        client_socket.sendall(validity[0])
                elif data[0] == "upload_empty":
                    f = open(data[1], 'w')
                    f.close()
                    root, dirs, files = next(os.walk(data[1][0:data[1].rfind("/")]))
                    send = []
                    send.append(File(".."))
                    for x in dirs:
                        send.append(Directory(x))
                    for x in files:
                        send.append(File(x))
                    client_socket.sendall(pickle.dumps(send))
        else:
            if data == "upload":
                client_socket.sendall("ok")
                size = pickle.loads(client_socket.recv(4096))
                client_socket.sendall("ok")
                path = pickle.loads(client_socket.recv(4096))
                client_socket.sendall("ok")
                written = 0
                l = client_socket.recv(1026)
                f = open(path, 'wb')
                while written < size:
                    if l[:2] == "no":
                        f.close()
                        os.remove(path)
                        break
                    f.write(l[2:])
                    written += len(l[2:])
                    if written >= size:
                        break
                    l = client_socket.recv(1026)
                if l[:2] != "no":
                    f.close()
                root, dirs, files = next(os.walk(path[0:path.rfind("/")]))
                send = []
                send.append(File(".."))
                for x in dirs:
                    send.append(Directory(x))
                for x in files:
                    send.append(File(x))
                client_socket.sendall(pickle.dumps(send))
            elif data == "download":
                client_socket.sendall("ok")
                path = pickle.loads(client_socket.recv(4096))
                size = os.path.getsize(path)
                client_socket.sendall(pickle.dumps(size))
                f = open(path, 'rb')
                l = f.read(1024)
                while (l):
                    client_socket.sendall(l)
                    data = client_socket.recv(1024)
                    if data == "no":
                        break
                    l = f.read(1024)
                f.close()
                print "Done."
class User(object):
    def __init__(this, username, email, password):
        this.username = username
        this.email = email
        this.password = password
def check_credentials(data):
    for x in users:
        if x.username == data[1] and x.password == data[2]:
            return True
    return False
def register(data):
    ret = []
    ret.append("")
    username_valid = True
    email_valid = True
    password_valid = True
    for x in users:
        if data[1] == x.username:
            username_valid = False
        if data[2] == x.email:
            email_valid = False
        if not username_valid and not email_valid:
            break
    if len(data[3]) <= 5:
        password_valid = False
    if not username_valid: ret[0]+="u"
    if not email_valid: ret[0]+="e"
    if not password_valid: ret[0]+="p"
    if username_valid and email_valid and password_valid:
        users.append(User(data[1], data[2], data[3]))
        ret.append(data[1])
        ret.append(data[2])
        ret.append(data[3])
    return ret
class File(object):
    def __init__(this, fileName):
        this.fileName = fileName
class Directory(object):
    def __init__(this, dirName):
        this.dirName = dirName
def exit():
    global clients
    for x in clients:
        x[0].close()
    server_socket.close()
    sys.exit()
    os._exit(0)
def acceptClients():
    global clients
    clients = []
    while True:
        (client_socket, client_address) = server_socket.accept()
        clients.append((client_socket, client_address))
        print str(client_address[0]) + ":" + str(client_address[1]) + " has connected."
        t = threading.Thread(target=clientthread, args=(client_socket, client_address,))
        t.daemon = True
        t.start()
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
t1 = threading.Thread(target=acceptClients)
t1.daemon = True
t1.start()
a = QtGui.QApplication(sys.argv)
w = Window()
a.exec_()


