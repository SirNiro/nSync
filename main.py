import sys, socket, os
import pickle
import errno
try:
    from PySide import QtGui, QtCore
except:
    os.system('pip install pyside')
    from PySide import QtGui, QtCore
ip = '127.0.0.1'
port = 8820
class File(object):
    def __init__(this, fileName):
        this.fileName = fileName
class Directory(object):
    def __init__(this, dirName):
        this.dirName = dirName
def main():
    global register_ins
    global login_ins
    global client_socket
    app = QtGui.QApplication(sys.argv)
    client_socket = socket.socket()
    try:
        client_socket.connect((ip, port))
    except:
        QtGui.QMessageBox.critical(None, "Error", "Could not connect to server.")
    register_ins = register_form()
    register_ins.center()
    login_ins = login_form()
    login_ins.center()
    login_ins.show()
    sys.exit(app.exec_())
class login_form(QtGui.QWidget):
    def __init__(this):
        super(login_form, this).__init__()
        global client_socket
        this.setupUi()
    def setupUi(this):
        this.resize(300, 200)
        this.setWindowTitle("Log-in")

        this.title_label = QtGui.QLabel(this)
        this.title_label.setGeometry(QtCore.QRect(120, 5, 60, 50))

        this.login_button = QtGui.QPushButton(this)
        this.login_button.setGeometry(QtCore.QRect(50, 135, 100, 50))
        this.login_button.clicked.connect(this.loginPressed)

        this.register_button = QtGui.QPushButton(this)
        this.register_button.setGeometry(QtCore.QRect(150, 135, 100, 50))
        this.register_button.clicked.connect(this.registerPressed)

        this.lineEdit = QtGui.QLineEdit(this)
        this.lineEdit.setGeometry(QtCore.QRect(120, 50, 120, 20))

        this.lineEdit_2 = QtGui.QLineEdit(this)
        this.lineEdit_2.setGeometry(QtCore.QRect(120, 90, 120, 20))
        this.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)

        this.username_label = QtGui.QLabel(this)
        this.username_label.setGeometry(QtCore.QRect(50, 50, 71, 21))

        this.password_label = QtGui.QLabel(this)
        this.password_label.setGeometry(QtCore.QRect(50, 90, 71, 21))

        this.forgot_button = QtGui.QPushButton(this)
        this.forgot_button.setGeometry(QtCore.QRect(115, 112, 100, 20))
        this.forgot_button.setFlat(True)
        this.forgot_button.setStyleSheet("text-decoration: underline")
        this.forgot_button.clicked.connect(this.forgotPressed)

        this.title_label.setText("NSync")
        this.title_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        this.login_button.setText("Log-in")
        this.register_button.setText("Register")
        this.username_label.setText("Username:")
        this.password_label.setText("Password:")
        this.forgot_button.setText("Forgot Password")
    def loginPressed(this):
        global client_socket
        login_info = ["login", this.lineEdit.text(), this.lineEdit_2.text()]
        try:
            client_socket.sendall(pickle.dumps(login_info))
            data = client_socket.recv(4096)
            if data == "login_unsuccessful":
                QtGui.QMessageBox.critical(None, "Error", "User credentials are incorrect, please try again.")
                this.lineEdit.setText("")
                this.lineEdit_2.setText("")
                this.lineEdit.setFocus()
            elif data == "login_successful":
                client_socket.sendall(login_info[1])
                client_socket.recv(1024)
                client_socket.sendall(pickle.dumps(["showDir","./users/" + login_info[1]+"/"]))
                data = pickle.loads(client_socket.recv(8192))
                this.upload_form = upload_form("./users/" + login_info[1]+"/", login_info[1])
                for x in data:
                    if isinstance(x, Directory):
                        this.upload_form.addDirectory(x.dirName)
                    else:
                        this.upload_form.addFile(x.fileName)
                this.upload_form.center()
                this.upload_form.show()
                this.close()
            else: raise StandardError # for linux
        except:
            try:
                client_socket = socket.socket()
                client_socket.connect((ip, port))
                this.loginPressed()
            except:
                QtGui.QMessageBox.critical(None, "Error", "Server is closed. Try again later")

    def center(this):
        qr = this.frameGeometry()  # gets a rectangle with the geometry of the window.
        cp = QtGui.QDesktopWidget().availableGeometry().center()  # the center point of the resolution of the monitor
        qr.moveCenter(cp)  # sets the center point of the rect to the center of the screen
        this.move(qr.topLeft())  # moves the top left point of the window to the top left point of the rect

    def registerPressed(this):
        global register_ins
        register_ins.center()
        register_ins.show()
        this.close()
    def forgotPressed(this):
        global client_socket
        username, ok = QtGui.QInputDialog.getText(this, "Forgot password", "Enter your username:")
        if ok:
            try:
                client_socket.sendall(pickle.dumps(["forgot_password1", username]))
                if client_socket.recv(1024) == "ok":
                    QtGui.QMessageBox.information(None, "", "Email with reset code has been sent.")
                    valid = False
                    while not valid:
                        code, ok = QtGui.QInputDialog.getText(this, "Forgot password", "Enter the reset code you received in the mail:")
                        if ok:
                            client_socket.sendall(pickle.dumps(["forgot_password2", username, code]))
                            if client_socket.recv(1024) == "valid":
                                valid = True
                            else:
                                QtGui.QMessageBox.critical(None, "Error", "Invalid reset code.")
                        else:
                            break
                    else:
                        valid = False
                        while not valid:
                            password, ok = QtGui.QInputDialog.getText(this, "Change password", "Enter a new password:")
                            if ok:
                                client_socket.sendall(pickle.dumps(["forgot_password3", username, password, code]))
                                if client_socket.recv(1024) == "changed":
                                    valid = True
                                    QtGui.QMessageBox.information(None, "Success", "Password has been changed.")
                                else:
                                    QtGui.QMessageBox.critical(None, "Error", "Password must be over 5 characters.")
                            else:
                                break
                else:
                    QtGui.QMessageBox.critical(None, "Error", "Username does not exist.")
            except:
                try:
                    client_socket = socket.socket()
                    client_socket.connect((ip, port))
                    QtGui.QMessageBox.critical(None, "Error", "Server is closed. Try again later")
                except:
                    QtGui.QMessageBox.critical(None, "Error", "Server is closed. Try again later")
class register_form(QtGui.QWidget):
    def __init__(this):
        super(register_form, this).__init__()
        global client_socket
        this.setupUi()
    def setupUi(this):
        this.resize(420, 300)
        this.setWindowTitle("Register")

        this.register_label = QtGui.QLabel(this)
        this.register_label.setGeometry(QtCore.QRect(170, 20, 71, 21))
        this.register_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

        this.label = QtGui.QLabel(this)
        this.label.setGeometry(QtCore.QRect(80, 75, 71, 20))

        this.label_2 = QtGui.QLabel(this)
        this.label_2.setGeometry(QtCore.QRect(100, 120, 46, 13))

        this.label_3 = QtGui.QLabel(this)
        this.label_3.setGeometry(QtCore.QRect(80, 155, 61, 20))

        this.register_button = QtGui.QPushButton(this)
        this.register_button.setGeometry(QtCore.QRect(150, 200, 111, 51))
        this.register_button.clicked.connect(this.registerPressed)

        this.back_button = QtGui.QPushButton(this)
        this.back_button.setGeometry(QtCore.QRect(10, 270, 61, 20))
        this.back_button.clicked.connect(this.backPressed)

        this.widget = QtGui.QWidget(this)
        this.widget.setGeometry(QtCore.QRect(150, 60, 161, 131))
        this.verticalLayout = QtGui.QVBoxLayout(this.widget)
        this.verticalLayout.setContentsMargins(0, 0, 0, 0)

        this.lineEdit = QtGui.QLineEdit(this.widget)
        this.verticalLayout.addWidget(this.lineEdit)
        this.wrong_user_label = QtGui.QLabel(this)
        this.wrong_user_label.setGeometry(QtCore.QRect(320, 75, 100, 20))
        this.wrong_user_label.setStyleSheet("color: red")

        this.lineEdit_2 = QtGui.QLineEdit(this.widget)
        this.verticalLayout.addWidget(this.lineEdit_2)
        this.wrong_email_label = QtGui.QLabel(this)
        this.wrong_email_label.setGeometry(QtCore.QRect(320, 120, 100, 20))
        this.wrong_email_label.setStyleSheet("color: red")

        this.lineEdit_3 = QtGui.QLineEdit(this.widget)
        this.lineEdit_3.setEchoMode(QtGui.QLineEdit.Password)
        this.verticalLayout.addWidget(this.lineEdit_3)
        this.wrong_password_label= QtGui.QLabel(this)
        this.wrong_password_label.setGeometry(QtCore.QRect(320, 155, 110, 58))
        this.wrong_password_label.setStyleSheet("color: red")

        this.register_label.setText("Register")
        this.label.setText("Username:")
        this.label_2.setText("E-mail:")
        this.label_3.setText("Password:")
        this.register_button.setText("Register")
        this.back_button.setText("Back")
    def backPressed(this):
        global login_ins
        login_ins.center()
        login_ins.show()
        this.close()
    def is_ascii(this, text):
        try:
            text.decode('ascii')
        except:
            return False
        else:
            return True
    def registerPressed(this):
        global client_socket
        if not this.is_ascii(this.lineEdit.text()) or not this.is_ascii(this.lineEdit_2.text()) or not this.is_ascii(this.lineEdit_3.text()):
            QtGui.QMessageBox.critical(None, "Error", "Can't have unicode in any of the fields.")
        else:
            if this.lineEdit.text() == "" or this.lineEdit_2.text() == "" or this.lineEdit_3.text() == "":
                QtGui.QMessageBox.critical(None, "Error", "Can't have empty fields.")
                if "@" not in this.lineEdit_2.text() or this.lineEdit_2.text() == "@":
                    QtGui.QMessageBox.critical(None, "Error", "Enter valid email address.")
            elif "@" not in this.lineEdit_2.text() or this.lineEdit_2.text() == "@":
                QtGui.QMessageBox.critical(None, "Error", "Enter valid email address.")
            else:
                this.wrong_user_label.setText("")
                this.wrong_email_label.setText("")
                this.wrong_password_label.setText("")
                register_info = ['register']
                register_info.append(this.lineEdit.text())
                register_info.append(this.lineEdit_2.text())
                register_info.append(this.lineEdit_3.text())
                try:
                    client_socket.sendall(pickle.dumps(register_info))
                    data = client_socket.recv(4096)
                    if data == 'u':
                        this.wrong_user_label.setText("Taken username")
                    elif data == 'ue':
                        this.wrong_user_label.setText("Taken username")
                        this.wrong_email_label.setText("Taken e-mail")
                    elif data == 'uep':
                        this.wrong_user_label.setText("Taken username")
                        this.wrong_email_label.setText("Taken e-mail")
                        this.wrong_password_label.setText("Password must\nbe above 5\ncharacters")
                    elif data == 'e':
                        this.wrong_email_label.setText("Taken e-mail")
                    elif data == 'p':
                        this.wrong_password_label.setText("Password must\nbe above 5\ncharacters")
                    elif data == 'ep':
                        this.wrong_email_label.setText("Taken e-mail")
                        this.wrong_password_label.setText("Password must\nbe above 5\ncharacters")
                    elif data == 'up':
                        this.wrong_user_label.setText("Taken username")
                        this.wrong_password_label.setText("Password must\nbe above 5\ncharacters")
                    elif data == 's':
                        QtGui.QMessageBox.information(None, "Success", "You have been registered, now login.")
                        login_ins.center()
                        login_ins.show()
                        this.close()
                    else:
                        raise StandardError # for linux
                except:
                    try:
                        client_socket = socket.socket()
                        client_socket.connect((ip, port))
                        this.registerPressed()
                    except:
                        QtGui.QMessageBox.critical(None, "Error", "Server is closed. Try again later")
    def center(this):
        qr = this.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        this.move(qr.topLeft())
class upload_form(QtGui.QWidget):
    def __init__(this, path, username):
        super(upload_form, this).__init__()
        this.path = path
        this.username = username
        global client_socket
        global lastpath
        lastpath = ""
        global uploading
        uploading = False
        global downloading
        downloading = False
        global stop
        stop = False
        this.uploadThread = UploadThread()
        this.downloadThread = DownloadThread()
        this.connect(this.uploadThread, QtCore.SIGNAL("uploadDone()"), this.uploadDone)
        this.connect(this.uploadThread, QtCore.SIGNAL("updateProgress()"), this.updateProgress)
        this.connect(this.downloadThread, QtCore.SIGNAL("updateProgress()"), this.updateProgress)
        this.connect(this.downloadThread, QtCore.SIGNAL("downloadDone()"), this.downloadDone)
        this.connect(this.uploadThread, QtCore.SIGNAL("failMsg()"), this.failMsg)
        this.connect(this.downloadThread, QtCore.SIGNAL("failMsg()"), this.failMsg)
        this.setAcceptDrops(True)
        this.setupUi()

    def dragEnterEvent(this, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(this, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(this, e):
        if e.mimeData().hasUrls:
            e.accept()
            # Workaround for OSx dragging and dropping
            urls = e.mimeData().urls()
            if len(urls) < 2:
                try:
                    fname = str(urls[0].toLocalFile())
                    if os.path.isfile(fname):
                        msgbox = QtGui.QMessageBox
                        ret = msgbox.question(this, 'Confirm', 'Are you sure you want to upload this file?',msgbox.Yes | msgbox.No)
                        if ret == msgbox.Yes:
                            this.lineEdit.setText(fname)
                            this.uploadPressed()
                except:
                    pass

        else:
            e.ignore()
    def setupUi(this):
        this.resize(480, 500)
        this.setWindowTitle(this.username)

        this.browse_button = QtGui.QPushButton(this)
        this.browse_button.setGeometry(QtCore.QRect(10, 10, 87, 35))
        this.browse_button.clicked.connect(this.browsePressed)

        this.createdir_button = QtGui.QPushButton(this)
        this.createdir_button.setGeometry(QtCore.QRect(103, 10, 87, 35))
        this.createdir_button.clicked.connect(this.createFolderPressed)


        this.rename_button = QtGui.QPushButton(this)
        this.rename_button.setGeometry(QtCore.QRect(196, 10, 87, 35))
        this.rename_button.clicked.connect(this.renamePressed)

        this.delete_button = QtGui.QPushButton(this)
        this.delete_button.setGeometry(QtCore.QRect(289, 10, 87, 35))
        this.delete_button.clicked.connect(this.deletePressed)

        this.download_button = QtGui.QPushButton(this)
        this.download_button.setGeometry(QtCore.QRect(382, 10, 87, 35))
        this.download_button.clicked.connect(this.downloadPressed)

        this.progressBar = QtGui.QProgressBar(this)
        this.progressBar.setGeometry(QtCore.QRect(10, 420, 460, 30))
        this.progressBar.setProperty("value", 0)

        this.upload_button = QtGui.QPushButton(this)
        this.upload_button.setGeometry(QtCore.QRect(200, 460, 85, 35))
        this.upload_button.clicked.connect(this.uploadPressed)

        this.logout_button = QtGui.QPushButton(this)
        this.logout_button.setGeometry(QtCore.QRect(420, 460, 50, 30))
        this.logout_button.clicked.connect(this.logoutPressed)

        this.refresh_button = QtGui.QPushButton(this)
        this.refresh_button.setGeometry(10, 460, 50, 30)
        this.refresh_button.clicked.connect(this.refreshPressed)

        this.cancel_button = QtGui.QPushButton(this)
        this.cancel_button.setGeometry(295, 462, 50, 30)
        this.cancel_button.clicked.connect(this.cancelPressed)
        this.cancel_button.hide()

        this.lineEdit = QtGui.QLineEdit(this)
        this.lineEdit.setGeometry(QtCore.QRect(10, 50, 460, 29))
        this.lineEdit.setReadOnly(True)

        this.file_list = QtGui.QListWidget(this)
        this.file_list.setGeometry(QtCore.QRect(10, 90, 460, 320))
        global diricon
        diricon = QtGui.QIcon()
        diricon.addPixmap(QtGui.QPixmap("if_folder_299060.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        this.file_list.itemDoubleClicked.connect(this.itemClicked)

        this.upload_button.setText("Upload")
        this.browse_button.setText("Browse")
        this.createdir_button.setText("Create Folder")
        this.rename_button.setText("Rename")
        this.delete_button.setText("Delete")
        this.download_button.setText("Download")
        this.logout_button.setText("Logout")
        this.refresh_button.setText("Refresh")
        this.cancel_button.setText("Cancel")

    def addDirectory(this, name):
        global diricon
        global dir
        dir = QtGui.QListWidgetItem(this.file_list)
        dir.setIcon(diricon)
        dir.setText(name+"/")
    def itemClicked(this):
        try:
            if this.file_list.selectedItems()[0].text()[-1] == "/":
                global uploading
                global downloading
                if uploading or downloading:
                    if uploading:
                        QtGui.QMessageBox.critical(None, "Error", "Must wait for upload to finish, or press cancel.")
                    if downloading:
                        QtGui.QMessageBox.critical(None, "Error", "Must wait for download to finish, or press cancel.")
                else:
                    newpath = this.path + this.file_list.selectedItems()[0].text()
                    global client_socket
                    client_socket.sendall(pickle.dumps(["showDir", newpath]))
                    data = pickle.loads(client_socket.recv(8192))
                    if data != "doesn't exist":
                        this.clearFileList(data)
                        this.path = newpath
                    else:
                        if this.path == "./users/" + this.username + "/":
                            QtGui.QMessageBox.critical(None, "Error","The folder you're trying to navigate to does not exist anymore.\nRefreshing..")
                        else:
                            QtGui.QMessageBox.critical(None, "Error","The folder you're trying to navigate to does not exist anymore.\nReturning to root.")
                            this.path = "./users/" + this.username + "/"
                        client_socket.sendall(pickle.dumps(["showDir", "./users/" + this.username + "/"]))
                        data = pickle.loads(client_socket.recv(8192))
                        this.clearFileList(data)
            elif this.file_list.selectedItems()[0].text() == "..":
                if this.path != "./users/" + this.username+"/":
                    if uploading or downloading:
                        if uploading:
                            QtGui.QMessageBox.critical(None, "Error", "Must wait for upload to finish, or press cancel.")
                        if downloading:
                            QtGui.QMessageBox.critical(None, "Error", "Must wait for download to finish, or press cancel.")
                    else:
                        newpath = this.path[:this.path.rfind("/")]
                        newpath = newpath[:newpath.rfind("/")+1]
                        client_socket.sendall(pickle.dumps(["showDir", newpath]))
                        data = pickle.loads(client_socket.recv(8192))
                        if data != "doesn't exist":
                            this.path = newpath
                            this.clearFileList(data)
                        else:
                            QtGui.QMessageBox.critical(None, "Error", "The folder you're trying to navigate to does not exist anymore.\nReturning to root.")
                            this.path = "./users/" + this.username + "/"
                            client_socket.sendall(pickle.dumps(["showDir", this.path]))
                            data = pickle.loads(client_socket.recv(8192))
                            this.clearFileList(data)
        except:
            QtGui.QMessageBox.critical(None, "Error", "Server is closed. Please try again later.")
            global login_ins
            login_ins.center()
            login_ins.show()
            this.close()

    def addFile(this, name):
        file = QtGui.QListWidgetItem(this.file_list)
        file.setText(name)
    def center(this):
        qr = this.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        this.move(qr.topLeft())
    def browsePressed(this):
        global lastpath
        filename = QtGui.QFileDialog.getOpenFileName(this, "Upload File", lastpath)
        if filename[0] != "":
            this.lineEdit.setText(filename[0])
            lastpath = filename[0]
            lastpath = lastpath[:lastpath.rfind("/") + 1]
    def createFolderPressed(this):
        try:
            global uploading
            global downloading
            if uploading or downloading:
                if uploading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for upload to finish, or press cancel.")
                if downloading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for download to finish, or press cancel.")
            else:
                dirName, ok = QtGui.QInputDialog.getText(this, 'Create a folder','Enter folder name:')
                valid = True
                if ok:
                    if dirName == "" :
                        valid = False
                        QtGui.QMessageBox.critical(None, "Error",'A folder\'s name can\'t be blank.')
                    elif "/" in dirName or "\\" in dirName or "?" in dirName or "|" in dirName or "*" in dirName or ":" in dirName or "<" in dirName or ">" in dirName or '"' in dirName or dirName[0] == ".":
                        valid = False
                        QtGui.QMessageBox.critical(None, "Error", 'A folder\'s name can\'t contain any of the following characters:\n \\ / : * ? " < > |, or begin with a dot.')
                    exists = False
                    if valid == True:
                        for x in xrange(this.file_list.count()):
                            if this.file_list.item(x).text() == dirName + "/" or this.file_list.item(x).text() == dirName :
                                exists = True
                                QtGui.QMessageBox.critical(None, "Error","A folder with that name already exists.")
                                break
                    if not exists and valid:
                        global client_socket
                        client_socket.sendall(pickle.dumps(["mkdir",this.path+dirName+"/"]))
                        data = pickle.loads(client_socket.recv(8192))
                        if data == "already exists":
                            QtGui.QMessageBox.critical(None, "Error","A folder with that name already exists.\nRefreshing..")
                            client_socket.sendall(pickle.dumps(["showDir", this.path]))
                            data = pickle.loads(client_socket.recv(8192))
                        this.clearFileList(data)
        except:
            QtGui.QMessageBox.critical(None, "Error", "Server is closed. Please try again later.")
            global login_ins
            login_ins.center()
            login_ins.show()
            this.close()
    def renamePressed(this):
        try:
            global uploading
            global downloading
            if uploading or downloading:
                if uploading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for upload to finish, or press cancel.")
                if downloading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for download to finish, or press cancel.")
            else:
                if this.file_list.selectedItems(): # if list is not empty
                    if this.file_list.selectedItems()[0].text() != "..":
                        if "/" in this.file_list.selectedItems()[0].text():
                            newName, ok = QtGui.QInputDialog.getText(this, 'Rename File/Directory', 'Enter a new name:', text=this.file_list.selectedItems()[0].text()[0:-1])
                        else:
                            newName, ok = QtGui.QInputDialog.getText(this, 'Rename File/Directory', 'Enter a new name:', text=this.file_list.selectedItems()[0].text())
                        valid = True
                        if ok:
                            if newName == "":
                                valid = False
                                QtGui.QMessageBox.critical(None, "Error",'A new name can\'t be blank.')
                            elif "/" in newName or "\\" in newName or "?" in newName or "|" in newName or "*" in newName or ":" in newName or "<" in newName or ">" in newName or '"' in newName or newName[0] == ".":
                                valid = False
                                QtGui.QMessageBox.critical(None, "Error",'A new name can\'t contain any of the following characters:\n \\ / : * ? " < > |, or begin with a dot.')
                            exists = False
                            if valid:
                                for x in xrange(this.file_list.count()):
                                    if this.file_list.item(x).text() == newName + "/":
                                        exists = True
                                        QtGui.QMessageBox.critical(None, "Error", "A file/folder with that name already exists.")
                                        break
                            if not exists and valid:
                                global client_socket
                                client_socket.sendall(pickle.dumps(["mv", this.path + this.file_list.selectedItems()[0].text(), this.path + newName]))
                                data = pickle.loads(client_socket.recv(8192))
                                if data == "already exists":
                                    QtGui.QMessageBox.critical(None, "Error", "A file/folder with that name already exists.\nRefreshing..")
                                    client_socket.sendall(pickle.dumps(["showDir", this.path]))
                                    data = pickle.loads(client_socket.recv(8192))
                                this.clearFileList(data)
        except:
            QtGui.QMessageBox.critical(None, "Error", "Server is closed. Please try again later.")
            global login_ins
            login_ins.center()
            login_ins.show()
            this.close()
    def deletePressed(this):
        try:
            global uploading
            global downloading
            if uploading or downloading:
                if uploading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for upload to finish, or press cancel.")
                if downloading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for download to finish, or press cancel.")
            else:
                print this.path
                if this.file_list.selectedItems(): # if list is not empty
                    if this.file_list.selectedItems()[0].text() != "..":
                        qm = QtGui.QMessageBox
                        ret = qm.question(this, 'Confirm', 'Are you sure you want to delete that file/folder?', qm.Yes | qm.No)
                        if ret == qm.Yes:
                            if "/" in this.file_list.selectedItems()[0].text():
                                client_socket.sendall(pickle.dumps(["rmdir", this.path + this.file_list.selectedItems()[0].text()]))
                            else:
                                print this.path + this.file_list.selectedItems()[0].text()
                                client_socket.sendall(pickle.dumps(["rm", this.path + this.file_list.selectedItems()[0].text()]))
                            data = pickle.loads(client_socket.recv(8192))
                            if data == "doesn't exist":
                                QtGui.QMessageBox.critical(None, "Error", "The file/folder you're trying to delete does not exist anymore.\nRefreshing..")
                                client_socket.sendall(pickle.dumps(["showDir", this.path]))
                                data = pickle.loads(client_socket.recv(8192))
                            this.clearFileList(data)
        except:
            QtGui.QMessageBox.critical(None, "Error", "Server is closed. Please try again later.")
            global login_ins
            login_ins.center()
            login_ins.show()
            this.close()
    def updateProgress(this):
        global percent
        this.progressBar.setValue(percent)
    def uploadPressed(this):
        try:
            global uploading
            global downloading
            if uploading or downloading:
                if uploading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for upload to finish, or press cancel.")
                if downloading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for download to finish, or press cancel.")
            else:
                global filepath
                filepath = this.lineEdit.text()
                exists = False
                if filepath != "":
                    for x in xrange(this.file_list.count()):
                        if this.file_list.item(x).text()[-1] == "/":
                            if this.file_list.item(x).text()[0:-1] == (filepath[filepath.rfind("/") + 1:]):
                                QtGui.QMessageBox.critical(None, "Error", "A file/folder with that name already exists.")
                                exists = True
                                break
                        else:
                            if this.file_list.item(x).text() == (filepath[filepath.rfind("/") + 1:]):
                                QtGui.QMessageBox.critical(None, "Error", "A file/folder with that name already exists.")
                                exists = True
                                break
                    if not exists:
                        global size
                        size = os.path.getsize(filepath)
                        if size != 0:
                            client_socket.sendall("upload")
                            client_socket.recv(1024)
                            client_socket.sendall(pickle.dumps(size))
                            size = float(size) / 1024
                            client_socket.recv(1024)
                            client_socket.sendall(pickle.dumps(this.path + (filepath[filepath.rfind("/") + 1:])))
                            data = client_socket.recv(1024)
                            if data == "doesn't exist":
                                QtGui.QMessageBox.critical(None, "Error", "The folder you're trying to upload to does not exist anymore.\nReturning to root..")
                                this.path = "./users/" + this.username + "/"
                                client_socket.sendall(pickle.dumps(["showDir", this.path]))
                                data = pickle.loads(client_socket.recv(8192))
                                this.clearFileList(data)
                            else:
                                this.progressBar.setValue(0)
                                uploading = True
                                this.uploadThread.start()
                                this.cancel_button.show()
                        else:
                            client_socket.sendall(pickle.dumps(["upload_empty",this.path + (filepath[filepath.rfind("/") + 1:])]))
                            data = pickle.loads(client_socket.recv(8192))
                            if data == "doesn't exist":
                                QtGui.QMessageBox.critical(None, "Error", "The folder you're trying to upload to does not exist anymore.\nReturning to root..")
                                this.path = "./users/" + this.username + "/"
                                client_socket.sendall(pickle.dumps(["showDir", this.path]))
                                data = pickle.loads(client_socket.recv(8192))
                                this.clearFileList(data)
                            else:
                                this.clearFileList(data)
                                this.lineEdit.setText("")
                                this.progressBar.setValue(100)
                                QtGui.QMessageBox.information(None, "Success", "Upload done!")
                else:
                    QtGui.QMessageBox.critical(None, "Error", "Select a path first by clicking the browse button.")
        except:
            QtGui.QMessageBox.critical(None, "Error", "Server is closed. Please try again later.")
            global login_ins
            login_ins.center()
            login_ins.show()
            this.close()
    def downloadPressed(this):
        try:
            global uploading
            global downloading
            if uploading or downloading:
                if uploading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for upload to finish, or press cancel.")
                if downloading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for download to finish, or press cancel.")
            else:
                if this.file_list.selectedItems():
                    if this.file_list.selectedItems()[0].text()[-1] != "/":
                        this.download_dialog = QtGui.QFileDialog()
                        global lastpath
                        global download_path
                        download_path = this.download_dialog.getSaveFileName(this, "Download File", lastpath+this.file_list.selectedItems()[0].text())
                        if download_path[0] != "":
                            lastpath = download_path[0]
                            lastpath = lastpath[:lastpath.rfind("/")+1]
                            print lastpath
                            client_socket.sendall("download")
                            client_socket.recv(1024)
                            client_socket.sendall(pickle.dumps(this.path+this.file_list.selectedItems()[0].text()))
                            global size
                            size = pickle.loads(client_socket.recv(1024))
                            client_socket.sendall("ok")
                            if size != "doesn't exist":
                                if size != "download_empty":
                                    this.progressBar.setValue(0)
                                    downloading = True
                                    this.downloadThread.start()
                                    this.cancel_button.show()
                                else:
                                    f = open(download_path[0], 'w')
                                    f.close()
                                    this.downloadDone()
                            else:
                                QtGui.QMessageBox.critical(None, "Error", "The file you're trying to download does not exist anymore.\nReturning to root..")
                                this.path = "./users/" + this.username + "/"
                                client_socket.sendall(pickle.dumps(["showDir", this.path]))
                                data = pickle.loads(client_socket.recv(8192))
                                this.clearFileList(data)
        except:
            QtGui.QMessageBox.critical(None, "Error", "Server is closed. Please try again later.")
            global login_ins
            login_ins.center()
            login_ins.show()
            this.close()
    def clearFileList(this, data):
        this.file_list.clear()
        for x in data:
            if isinstance(x, Directory):
                this.addDirectory(x.dirName)
            else:
                this.addFile(x.fileName)
    def logoutPressed(this):
        global uploading
        global downloading
        if uploading or downloading:
            if uploading:
                QtGui.QMessageBox.critical(None, "Error", "Must wait for upload to finish, or press cancel.")
            if downloading:
                QtGui.QMessageBox.critical(None, "Error", "Must wait for download to finish, or press cancel.")
        else:
            global login_ins
            login_ins.center()
            login_ins.show()
            this.close()
    def refreshPressed(this):
        try:
            global uploading
            global downloading
            if uploading or downloading:
                if uploading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for upload to finish, or press cancel.")
                if downloading:
                    QtGui.QMessageBox.critical(None, "Error", "Must wait for download to finish, or press cancel.")
            else:
                client_socket.sendall(pickle.dumps(["showDir", this.path]))
                data = pickle.loads(client_socket.recv(8192))
                if data == "doesn't exist":
                    QtGui.QMessageBox.critical(None, "Error","The folder you're trying to refresh does not exist anymore.\nReturning to root.")
                    this.path = "./users/" + this.username + "/"
                    client_socket.sendall(pickle.dumps(["showDir", this.path]))
                    data = pickle.loads(client_socket.recv(8192))
                this.clearFileList(data)
        except:
            QtGui.QMessageBox.critical(None, "Error", "Server is closed. Please try again later.")
            global login_ins
            login_ins.center()
            login_ins.show()
            this.close()
    def cancelPressed(this):
        global stop
        stop = True
    def uploadDone(this):
        try:
            data = pickle.loads(client_socket.recv(8192))
            this.clearFileList(data)
            this.lineEdit.setText("")
            global stop
            global uploading
            if stop:
                this.progressBar.setValue(0)
                QtGui.QMessageBox.information(None, "", "Upload canceled.")
                stop = False
            else:
                this.progressBar.setValue(100)
                QtGui.QMessageBox.information(None, "Success", "Upload done!")
            uploading = False
            this.cancel_button.hide()
        except:
            QtGui.QMessageBox.critical(None, "Error", "Server is closed. Please try again later.")
            global login_ins
            login_ins.center()
            login_ins.show()
            this.close()
    def downloadDone(this):
        global stop
        global downloading
        if stop:
            this.progressBar.setValue(0)
            QtGui.QMessageBox.information(None, "", "Download canceled.")
            stop = False
        else:
            this.progressBar.setValue(100)
            QtGui.QMessageBox.information(None, "Success", "Download done!")
        downloading = False
        this.cancel_button.hide()
    def failMsg(this):
        QtGui.QMessageBox.critical(None, "Error", "Server is closed. Please try again later.")
        global login_ins
        login_ins.center()
        login_ins.show()
        this.close()
class UploadThread(QtCore.QThread):
    def __init__(this ,parent=None):
        super(UploadThread, this).__init__(parent)
    def run(this):
        try:
            global size
            global stop
            f = open(filepath, 'rb')
            l = f.read(1024)
            written = 0
            global percent
            while (l):
                if stop:
                    client_socket.sendall("no")
                    break
                else:
                    client_socket.sendall("ok" + l)
                    l = f.read(1024)
                    written += float(len(l)/1024)
                    percent = int(float(written) / float(size) * 100)
                    this.emit(QtCore.SIGNAL("updateProgress()"))
            f.close()
            print "Done."
            this.emit(QtCore.SIGNAL("uploadDone()"))
        except:
            this.emit(QtCore.SIGNAL("failMsg()"))



class DownloadThread(QtCore.QThread):
    def __init__(this ,parent=None):
        super(DownloadThread, this).__init__(parent)
    def run(this):
        try:
            global percent
            written = 0
            l = client_socket.recv(1026)
            client_socket.sendall("ok")
            f = open(download_path[0], 'wb')
            global stop
            while written <= size:
                if stop:
                    client_socket.recv(1024)
                    client_socket.sendall("no")
                    f.close()
                    os.remove(download_path[0])
                    break
                f.write(l)
                written += len(l)
                percent = int(float(written)/ float(size) * 100)
                this.emit(QtCore.SIGNAL("updateProgress()"))
                if written >= size:
                    break
                l = client_socket.recv(1026)
                client_socket.sendall("ok")
            if not stop:
                f.close()
            print "Done."
            this.emit(QtCore.SIGNAL("downloadDone()"))
        except:
            this.emit(QtCore.SIGNAL("failMsg()"))
main()