import os
import sys
import socket
import pickle
import threading
import shutil
import urllib
import random as rand
from functools import partial
try:
    from PySide import QtGui, QtCore
except:
    os.system('pip install pyside')
    from PySide import QtGui, QtCore
if not os.path.exists("if_folder_299060.png"):
    try:
        urllib.urlretrieve("https://drive.google.com/uc?id=1tcSrcRpZZ3fgSrWcIHoNyqhw7DHd7Evy&export=download", "if_folder_299060.png")
    except:
        pass
if not os.path.exists("if_user-alt_285645.png"):
    try:
        urllib.urlretrieve("https://drive.google.com/uc?id=1JQ_xmjDDVJyCYsppf4psTtK8gyu8ggih&export=download", "if_user-alt_285645.png")
    except:
        pass
import uuid, smtplib
import time
uuid_dict = {}
class Window(QtGui.QWidget):

    def __init__(this):
        super(Window, this).__init__()
        this.initUI()



    def initUI(this):
        this.resize(300, 300)
        this.setWindowTitle('Server Panel')
        this.setWindowIcon(QtGui.QIcon('archlinux-512'))

        global serveropen
        serveropen = True

        this.title_label = QtGui.QLabel(this)
        this.title_label.setGeometry(QtCore.QRect(50, -20, 220, 80))

        this.users_button = QtGui.QPushButton(this)
        this.users_button.setGeometry(QtCore.QRect(100, 40, 100, 50))
        this.users_button.clicked.connect(this.usersPressed)

        this.logs_button = QtGui.QPushButton(this)
        this.logs_button.setGeometry(QtCore.QRect(100, 130, 100, 50))
        this.logs_button.clicked.connect(this.logsPressed)

        this.close_button = QtGui.QPushButton(this)
        this.close_button.setGeometry(QtCore.QRect(100, 230, 100, 50))
        this.close_button.clicked.connect(partial(exit,this.close_button))

        this.title_label.setText("NSync Server Panel")
        this.title_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        this.users_button.setText("View Users")
        this.logs_button.setText("View Logs")
        this.close_button.setText("Close Server")

    def center(this):
        qr = this.frameGeometry()  # gets a rectangle with the geometry of the window.
        cp = QtGui.QDesktopWidget().availableGeometry().center()  # the center point of the resolution of the monitor
        qr.moveCenter(cp)  # sets the center point of the rect to the center of the screen
        this.move(qr.topLeft())  # moves the top left point of the window to the top left point of the rect

    def usersPressed(this):
        us.refresh()
        us.center()
        us.show()
        this.close()
    def logsPressed(this):
        lw.center()
        lw.show()
        this.close()
class usersWindow(QtGui.QWidget):
    def __init__(this):
        super(usersWindow, this).__init__()
        global users
        this.initUI()

    def initUI(this):
        this.resize(500, 500)
        this.setWindowTitle('Users List')
        this.setWindowIcon(QtGui.QIcon('archlinux-512'))

        this.back_button = QtGui.QPushButton(this)
        this.back_button.setGeometry(QtCore.QRect(5, 475, 61, 20))
        this.back_button.clicked.connect(this.backPressed)
        this.refresh_button = QtGui.QPushButton(this)
        this.refresh_button.setGeometry(QtCore.QRect(230, 475, 61, 20))
        this.refresh_button.clicked.connect(this.refresh)
        global icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("if_user-alt_285645.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        this.user_list = QtGui.QTableWidget(this)
        this.user_list.setGeometry(QtCore.QRect(10, 10, 480, 460))
        this.user_list.setRowCount(len(users))
        this.user_list.setColumnCount(5)
        this.user_list.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem(""))
        this.user_list.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Username"))
        this.user_list.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("E-mail"))
        this.user_list.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem(""))
        this.user_list.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem(""))
        this.user_list.verticalHeader().hide()
        global view_buttons
        global ban_buttons
        view_buttons = []
        ban_buttons = []
        for x in range(len(users)):
            this.user_list.setItem(x, 0, QtGui.QTableWidgetItem(icon,""))
            this.user_list.setItem(x, 1, QtGui.QTableWidgetItem(users[x].username))
            this.user_list.setItem(x, 2, QtGui.QTableWidgetItem(users[x].email))
            b1 = QtGui.QPushButton("View Files")
            b1.clicked.connect(partial(this.viewFiles,x))
            view_buttons.append(b1)
            b2 = QtGui.QPushButton("Ban")
            b2.clicked.connect(partial(this.ban, x))
            ban_buttons.append(b2)
            this.user_list.setCellWidget(x, 3, b1)
            this.user_list.setCellWidget(x, 4, b2)
        this.user_list.resizeColumnsToContents()

        this.user_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        this.user_list.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        this.user_list.setShowGrid(False)
        this.back_button.setText("Back")
        this.refresh_button.setText("Refresh")
    def refresh(this):
        global view_buttons
        global ban_buttons
        this.user_list.setRowCount(len(users))
        for x in range(len(users)):
            this.user_list.setItem(x, 0, QtGui.QTableWidgetItem(icon,""))
            this.user_list.setItem(x, 1, QtGui.QTableWidgetItem(users[x].username))
            this.user_list.setItem(x, 2, QtGui.QTableWidgetItem(users[x].email))
            b1 = QtGui.QPushButton("View Files")
            b1.clicked.connect(partial(this.viewFiles,x))
            view_buttons.append(b1)
            b2 = QtGui.QPushButton("Ban")
            b2.clicked.connect(partial(this.ban, x))
            ban_buttons.append(b2)
            this.user_list.setCellWidget(x, 3, b1)
            this.user_list.setCellWidget(x, 4, b2)
        this.user_list.resizeColumnsToContents()
    def viewFiles(this, column):
        if len(users) != 0:
            name = this.user_list.item(column, 1).text()
            root, dirs, files = next(os.walk("./users/" + name+"/"))
            list = []
            for x in dirs:
                list.append(Directory(x))
            for x in files:
                list.append(File(x))
            this.form = upload_form("./users/" + name+"/", name)
            for x in list:
                if isinstance(x, Directory):
                    this.form.addDirectory(x.dirName)
                else:
                    this.form.addFile(x.fileName)
        this.form.center()
        this.form.show()
    def ban(this, row):
        msgbox = QtGui.QMessageBox
        ret = msgbox.question(this, 'Confirm', 'Are you sure you want to ban this user?', msgbox.Yes | msgbox.No)
        if ret == msgbox.Yes:
            name = this.user_list.item(row, 1).text()
            shutil.rmtree("./users/" + name + "/")
            f = open("database.txt", "r")
            lines = f.readlines()
            f.close()
            count = 0
            for line in lines:
                l1, l2, l3 = line.split()
                if l1 == name:
                    del lines[count]
                    break
                count += 1
            f = open("database.txt", "w")
            for line in lines:
                if line == lines[-1]:
                    f.write(line[:-1])
                else:
                    f.write(line)
            f.close()
            for x in users:
                if x.username == name:
                    users.remove(x)
                    if (x.s != None):
                        x.s.close()
                    break
            this.user_list.removeRow(row)
            QtGui.QMessageBox.information(None, "Success", "User has been banned")
    def center(this):
        qr = this.frameGeometry()  # gets a rectangle with the geometry of the window.
        cp = QtGui.QDesktopWidget().availableGeometry().center()  # the center point of the resolution of the monitor
        qr.moveCenter(cp)  # sets the center point of the rect to the center of the screen
        this.move(qr.topLeft())  # moves the top left point of the window to the top left point of the rect
    def backPressed(this):
        w.center()
        w.show()
        this.close()
def expiry(user, code):
    time.sleep(300)  # 5 minutes
    try:
        uuid_dict[user.username].remove(code)
    except:
        pass
class upload_form(QtGui.QWidget):
    def __init__(this, path, username):
        super(upload_form, this).__init__()
        this.path = path
        this.username = username
        global lastpath
        lastpath = ""
        global stop
        stop = False
        this.setupUi()

    def setupUi(this):
        this.resize(300, 400)
        this.setWindowTitle(this.username)

        this.refresh_button = QtGui.QPushButton(this)
        this.refresh_button.setGeometry(110, 355, 80, 40)
        this.refresh_button.clicked.connect(this.refreshPressed)
        this.file_list = QtGui.QListWidget(this)
        this.file_list.setGeometry(QtCore.QRect(10, 30, 280, 320))
        global diricon
        diricon = QtGui.QIcon()
        diricon.addPixmap(QtGui.QPixmap("if_folder_299060.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        this.file_list.itemDoubleClicked.connect(this.itemClicked)

        this.refresh_button.setText("Refresh")

    def addDirectory(this, name):
        global diricon
        global dir
        dir = QtGui.QListWidgetItem(this.file_list)
        dir.setIcon(diricon)
        dir.setText(name+"/")

    def addFile(this, name):
        file = QtGui.QListWidgetItem(this.file_list)
        file.setText(name)
    def center(this):
        qr = this.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        this.move(qr.topLeft())
    def clearFileList(this, data):
        this.file_list.clear()
        for x in data:
            if isinstance(x, Directory):
                this.addDirectory(x.dirName)
            else:
                this.addFile(x.fileName)
    def itemClicked(this):
        if this.file_list.selectedItems()[0].text()[-1] == "/":
            try:
                root, dirs, files = next(os.walk(this.path+ this.file_list.selectedItems()[0].text()))
                this.path = this.path + this.file_list.selectedItems()[0].text()
                this.file_list.clear()
                list = []
                if this.path != "./users/"+ this.username +"/":
                    list.append(File(".."))
                for x in dirs:
                    list.append(Directory(x))
                for x in files:
                    list.append(File(x))
                for x in list:
                    if isinstance(x, Directory):
                        this.addDirectory(x.dirName)
                    else:
                        this.addFile(x.fileName)
            except:
                if this.path == "./users/"+ this.username +"/":
                    QtGui.QMessageBox.critical(None, "Error", "The folder does not exist anymore.\nRefreshing..")
                else:
                    QtGui.QMessageBox.critical(None, "Error", "The folder does not exist anymore.\nReturning to root..")
                    this.path = "./users/"+ this.username +"/"
                root, dirs, files = next(os.walk(this.path))
                this.file_list.clear()
                list = []
                if this.path != "./users/" + this.username + "/":
                    list.append(File(".."))
                for x in dirs:
                    list.append(Directory(x))
                for x in files:
                    list.append(File(x))
                for x in list:
                    if isinstance(x, Directory):
                        this.addDirectory(x.dirName)
                    else:
                        this.addFile(x.fileName)

        elif this.file_list.selectedItems()[0].text()== "..":
            if this.path != "./users/" + this.username +"/":
                this.path = this.path[:this.path.rfind("/")]
                this.path = this.path[:this.path.rfind("/") + 1]
                try:
                    root, dirs, files = next(os.walk(this.path))
                    this.file_list.clear()
                    list = []
                    if this.path != "./users/" + this.username + "/":
                        list.append(File(".."))
                    for x in dirs:
                        list.append(Directory(x))
                    for x in files:
                        list.append(File(x))
                    for x in list:
                        if isinstance(x, Directory):
                            this.addDirectory(x.dirName)
                        else:
                            this.addFile(x.fileName)
                except:
                    QtGui.QMessageBox.critical(None, "Error", "The folder does not exist anymore.\nReturning to root..")
                    this.path = "./users/" + this.username + "/"
                    root, dirs, files = next(os.walk(this.path))
                    this.file_list.clear()
                    list = []
                    if this.path != "./users/" + this.username + "/":
                        list.append(File(".."))
                    for x in dirs:
                        list.append(Directory(x))
                    for x in files:
                        list.append(File(x))
                    for x in list:
                        if isinstance(x, Directory):
                            this.addDirectory(x.dirName)
                        else:
                            this.addFile(x.fileName)
    def refreshPressed(this):
        try:
            root, dirs, files = next(os.walk(this.path))
            this.file_list.clear()
            list = []
            if this.path != "./users/" + this.username + "/":
                list.append(File(".."))
            for x in dirs:
                list.append(Directory(x))
            for x in files:
                list.append(File(x))
            for x in list:
                if isinstance(x, Directory):
                    this.addDirectory(x.dirName)
                else:
                    this.addFile(x.fileName)
        except:
            QtGui.QMessageBox.critical(None, "Error", "The folder does not exist anymore.\nReturning to root..")
            this.path = "./users/" + this.username + "/"
            root, dirs, files = next(os.walk(this.path))
            this.file_list.clear()
            list = []
            if this.path != "./users/" + this.username + "/":
                list.append(File(".."))
            for x in dirs:
                list.append(Directory(x))
            for x in files:
                list.append(File(x))
            for x in list:
                if isinstance(x, Directory):
                    this.addDirectory(x.dirName)
                else:
                    this.addFile(x.fileName)
class logs_form(QtGui.QWidget):
    def __init__(this):
        super(logs_form, this).__init__()
        this.setupUi()

    def setupUi(this):
        this.resize(350, 400)
        this.setWindowTitle("Logs")
        this.back_button = QtGui.QPushButton(this)
        this.back_button.setGeometry(QtCore.QRect(10, 360, 61, 30))
        this.back_button.clicked.connect(this.backPressed)
        this.log_list = QtGui.QListWidget(this)
        this.log_list.setGeometry(QtCore.QRect(10, 30, 330, 320))
        this.log_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        this.back_button.setText("Back")
    def center(this):
        qr = this.frameGeometry()  # gets a rectangle with the geometry of the window.
        cp = QtGui.QDesktopWidget().availableGeometry().center()  # the center point of the resolution of the monitor
        qr.moveCenter(cp)  # sets the center point of the rect to the center of the screen
        this.move(qr.topLeft())  # moves the top left point of the window to the top left point of the rect
    def backPressed(this):
        w.center()
        w.show()
        this.close()
def clientthread(client_socket,client_address):
    global f
    global uploading
    uploading = False
    global path
    global serveropen
    while True:
        try:
            data = client_socket.recv(4096)
            if not serveropen:
                client_socket.close()
                break
        except:
            log = QtGui.QListWidgetItem(lw.log_list)
            log.setText(str(client_address[0]) + ":" + str(client_address[1]) + " has disconnected.")
            client_socket.close()
            break
        if not data:
            log = QtGui.QListWidgetItem(lw.log_list)
            log.setText(str(client_address[0]) + ":" + str(client_address[1]) + " has disconnected.")
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
                        client_socket.sendall(pickle.dumps("doesn't exist"))
                elif data[0] == "mkdir":
                    try:
                        username = data[1]
                        username = username[username.find("/")+1:]
                        username = username[username.find("/")+1:]
                        username = username[:username.find("/")]
                        name = data[1]
                        name = name[:name.rfind("/")]
                        name = name[name.rfind("/")+1:]
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
                        log = QtGui.QListWidgetItem(lw.log_list)
                        log.setText(username + " has created a folder named: " + name)
                    except WindowsError:
                        client_socket.sendall(pickle.dumps("already exists"))
                    except:
                        pass
                elif data[0] == "rmdir":
                    try:
                        username = data[1]
                        username = username[username.find("/")+1:]
                        username = username[username.find("/")+1:]
                        username = username[:username.find("/")]
                        name = data[1]
                        name = name[:name.rfind("/")]
                        name = name[name.rfind("/")+1:]
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
                        log = QtGui.QListWidgetItem(lw.log_list)
                        log.setText(username + " has deleted a folder named: " + name)
                    except WindowsError:
                        client_socket.sendall(pickle.dumps("doesn't exist"))
                    except:
                        pass
                elif data[0] == "rm":
                    try:
                        username = data[1]
                        username = username[username.find("/")+1:]
                        username = username[username.find("/")+1:]
                        username = username[:username.find("/")]
                        name = data[1]
                        name = name[name.rfind("/")+1:]
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
                        log = QtGui.QListWidgetItem(lw.log_list)
                        log.setText(username + " has deleted a file named: " + name)
                    except WindowsError:
                        client_socket.sendall(pickle.dumps("doesn't exist"))
                    except:
                        pass
                elif data[0] == "mv":
                    try:
                        if data[1][-1] == "/":
                            folder = True
                        else:
                            folder = False
                        username = data[1]
                        username = username[username.find("/")+1:]
                        username = username[username.find("/")+1:]
                        username = username[:username.find("/")]
                        name = data[1]
                        name1 = data[2]
                        if folder:
                            name = name[:name.rfind("/")]
                            name = name[name.rfind("/") + 1:]
                            name1 = name1[:name1.rfind("/")]
                            name1 = name1[name1.rfind("/") + 1:]
                        else:
                            name = name[name.rfind("/") + 1:]
                            name1 = name1[name1.rfind("/") + 1:]

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
                        log = QtGui.QListWidgetItem(lw.log_list)
                        if folder:
                            log.setText(username + " has renamed a folder named: " + name + " to: " + name1)
                        else:
                            log.setText(username + " has renamed a file named: " + name + " to: " + name1)
                    except WindowsError:
                        client_socket.sendall(pickle.dumps("already exists"))
                    except:
                        pass
                elif data[0] == "login":
                    if check_credentials(data):
                        client_socket.sendall("login_successful")
                        username = client_socket.recv(4096)
                        client_socket.sendall("ok")
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
                    validity = register(data, client_socket)
                    if validity[0] == "":
                        client_socket.sendall("s")
                        log = QtGui.QListWidgetItem(lw.log_list)
                        log.setText("A new user named: " + data[1] + " has been registered")
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
                    try:
                        username = data[1]
                        username = username[username.find("/")+1:]
                        username = username[username.find("/")+1:]
                        username = username[:username.find("/")]
                        name = data[1]
                        name = name[name.rfind("/")+1:]
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
                        log = QtGui.QListWidgetItem(lw.log_list)
                        log.setText(username + " has uploaded a new file named: " + name)
                    except:
                        client_socket.sendall(pickle.dumps("doesn't exist"))
        else:
            if data == "upload":
                uploading = True
                exception = False
                upload_socket = socket.socket()
                while True:
                    upload_port = rand.randint(8821, 9000)
                    try:
                        upload_socket.bind(('0.0.0.0', upload_port))
                        client_socket.sendall(str(upload_port))
                        upload_socket.listen(1)
                        (cupload_socket, cupload_address) = upload_socket.accept()
                        break
                    except:
                        pass
                path = pickle.loads(client_socket.recv(4096))
                username = path
                username = username[username.find("/") + 1:]
                username = username[username.find("/") + 1:]
                username = username[:username.find("/")]
                name = path
                name = name[name.rfind("/") + 1:]
                try:
                    f = open(path, 'wb')
                except:
                    exception = True
                    client_socket.sendall("doesn't exist")
                if not exception:
                    client_socket.send("exists")
                    l = cupload_socket.recv(1024)
                    cupload_socket.send("ok")
                    a = client_socket.recv(1024)
                    client_socket.send("ok")
                    while (l):
                        if a == "no":
                            break
                        f.write(l)
                        l = cupload_socket.recv(1024)
                        cupload_socket.send("ok")
                        a = client_socket.recv(1024)
                        client_socket.send("ok")
                    f.close()
                    if a == "no":
                        os.remove(path)
                    else:
                        log = QtGui.QListWidgetItem(lw.log_list)
                        log.setText(username + " has uploaded a new file named: " + name)
                upload_socket.close()
                uploading = False

            elif data == "download":
                client_socket.sendall("ok")
                path = pickle.loads(client_socket.recv(8192))
                username = path
                username = username[username.find("/") + 1:]
                username = username[username.find("/") + 1:]
                username = username[:username.find("/")]
                name = path
                name = name[name.rfind("/") + 1:]
                download_empty = False
                try:
                    size = os.path.getsize(path)
                    if size == 0:
                        download_empty = True
                        client_socket.sendall("download_empty")
                    if not download_empty:
                        client_socket.sendall("exists")
                        client_socket.recv(1024)
                        client_socket.sendall(pickle.dumps(size))
                        port = client_socket.recv(1024)
                        download_socket = socket.socket()
                        download_socket.connect((client_address[0], int(port)))
                        f = open(path, 'rb')
                        a = "ok"
                        l = f.read(1024)
                        while l and a:
                            download_socket.sendall(l)
                            a = download_socket.recv(1024)
                            l = f.read(1024)
                        f.close()
                        download_socket.close()
                        if a:
                            log = QtGui.QListWidgetItem(lw.log_list)
                            log.setText(username + " has downloaded a file named: " + name)

                except:
                    client_socket.sendall("doesn't exist")


class User(object):
    def __init__(this, username, email, password, s=None):
        this.username = username
        this.email = email
        this.password = password
        this.s = s
def check_credentials(data):
    for x in users:
        if x.username == data[1] and x.password == data[2]:
            return True
    return False
def register(data, client_socket):
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
        users.append(User(data[1], data[2], data[3], client_socket))
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
def exit(close_button):
    global serveropen
    global uploading
    global t1
    global server_socket
    if serveropen:
        if uploading:
            f.close()
            os.remove(path)
        global clients
        for x in clients:
            x[0].close()
        del clients[:]
        server_socket.close()
        temp_socket = socket.socket()
        temp_socket.connect(("127.0.0.1", 8820))
        temp_socket.close()
        close_button.setText("Open Server")
    else:
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', 8820))
        server_socket.listen(100)
        uploading = False
        t1 = threading.Thread(target=acceptClients)
        t1.daemon = True
        t1.start()
        close_button.setText("Close Server")
    serveropen = not serveropen
def acceptClients():
    global clients
    clients = []
    global serveropen
    global server_socket
    while True:
        (client_socket, client_address) = server_socket.accept()
        if not serveropen:
            break
        clients.append((client_socket, client_address))
        log = QtGui.QListWidgetItem(lw.log_list)
        log.setText(str(client_address[0]) + ":" + str(client_address[1]) + " has connected.")
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
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 8820))
server_socket.listen(100)
global uploading
uploading = False
global t1
t1 = threading.Thread(target=acceptClients)
t1.daemon = True
t1.start()
a = QtGui.QApplication(sys.argv)
w = Window()
us = usersWindow()
lw = logs_form()
w.show()
a.exec_()


