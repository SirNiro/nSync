import sys, socket, pickle
from PySide import QtCore, QtGui
from threading import *
ip = '10.0.0.9'
port = 8820
class File(object):
    def __init__(this, fileName):
        this.fileName = fileName
class Directory(object):
    def __init__(this, dirName, files):
        this.dirName = dirName
        this.files = files
class Window(QtGui.QWidget):

    def __init__(this):
        super(Window, this).__init__()
        this.initUI()

    def initUI(this):
        this.setGeometry(300, 300, 250, 150)
        this.setWindowTitle('Icon')
        this.setWindowIcon(QtGui.QIcon('archlinux-512'))

        this.show()
def main():
    global register_ins
    global login_ins
    global client_socket
    app = QtGui.QApplication(sys.argv)
    client_socket = socket.socket()
    try:
        client_socket.connect((ip, port))
    except:
        QtGui.QMessageBox.critical(None, "Error", "Could not connect to server. Please try again in a few minutes.")
        sys.exit()
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
        this.setObjectName("Form")
        this.resize(300, 200)

        this.title_label = QtGui.QLabel(this)
        this.title_label.setGeometry(QtCore.QRect(120, 5, 60, 50))

        this.login_button = QtGui.QPushButton(this)
        this.login_button.setGeometry(QtCore.QRect(50, 130, 100, 50))
        this.login_button.clicked.connect(this.loginPressed)

        this.register_button = QtGui.QPushButton(this)
        this.register_button.setGeometry(QtCore.QRect(150, 130, 100, 50))
        this.register_button.clicked.connect(this.registerPressed)

        this.lineEdit = QtGui.QLineEdit(this)
        this.lineEdit.setGeometry(QtCore.QRect(120, 50, 120, 20))
        this.lineEdit.setObjectName("lineEdit")

        this.lineEdit_2 = QtGui.QLineEdit(this)
        this.lineEdit_2.setGeometry(QtCore.QRect(120, 90, 120, 20))
        this.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)

        this.username_label = QtGui.QLabel(this)
        this.username_label.setGeometry(QtCore.QRect(50, 50, 71, 21))

        this.password_label = QtGui.QLabel(this)
        this.password_label.setGeometry(QtCore.QRect(50, 90, 71, 21))

        this.error_label = QtGui.QLabel(this)
        this.error_label.setGeometry(QtCore.QRect(200, 200, 100, 16))
        this.error_label.setStyleSheet("color: black");

        this.setWindowTitle("Log-in")

        this.title_label.setText("NSync")
        this.title_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        this.login_button.setText("Log-in")
        this.register_button.setText("Register")
        this.username_label.setText("Username:")
        this.password_label.setText("Password:")

    def loginPressed(this):
        global client_socket
        login_info = []
        login_info.append(this.lineEdit.text())
        login_info.append(this.lineEdit_2.text())
        try:
            client_socket.sendall(pickle.dumps(login_info))
            data = client_socket.recv(4096)
            if data == "login_unsuccessful":
                QtGui.QMessageBox.critical(None, "Error", "User credentials are incorrect, please try again.")
                this.lineEdit.setText("")
                this.lineEdit_2.setText("")
                this.lineEdit.setFocus()
            elif data == "login_successful":
                client_socket.sendall(pickle.dumps(["showDir","./users/" + login_info[0]+"/"]))
                data = pickle.loads(client_socket.recv(4096))
                this.close()
                this.upload_form = upload_form("./users/" + login_info[0]+"/", login_info[0])
                for x in data:
                    if isinstance(x, Directory):
                        this.upload_form.addDirectory(x.dirName)
                    else:
                        this.upload_form.addFile(x.fileName)
                this.upload_form.center()

                this.upload_form.show()
            else: raise StandardError # for linux
        except:
            try:
                client_socket = socket.socket()
                client_socket.connect((ip, port))
                this.loginPressed()
            except:
                QtGui.QMessageBox.critical(None, "Error", "Server is closed. Try again later")

    def center(this):

        qr = this.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        this.move(qr.topLeft())


    def registerPressed(this):
        global register_ins
        this.show()
        register_ins.center()
        register_ins.show()




class register_form(QtGui.QWidget):
    def __init__(this):
        super(register_form, this).__init__()
        global client_socket
        this.setupUi()
    def setupUi(this):
        this.setObjectName("Register")
        this.resize(420, 300)
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

        this.setWindowTitle("Register")
        this.register_label.setText("Register")
        this.label.setText("Username:")
        this.label_2.setText("E-mail:")
        this.label_3.setText("Password:")
        this.register_button.setText("Register")
        this.back_button.setText("Back")
    def backPressed(this):
        global login_ins
        this.close()
        login_ins.center()
        login_ins.show()
    def registerPressed(this):
        global client_socket
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
            register_info = []
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
                    this.close()
                    login_ins.center()
                    login_ins.show()
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
        this.setupUi()
    def setupUi(this):
        this.setObjectName("Form")
        this.resize(480, 495)


        this.progressBar = QtGui.QProgressBar(this)
        this.progressBar.setGeometry(QtCore.QRect(10, 420, 460, 30))
        this.progressBar.setProperty("value", 0)

        this.upload_button = QtGui.QPushButton(this)
        this.upload_button.setGeometry(QtCore.QRect(200, 460, 85, 35))

        this.browse_button = QtGui.QPushButton(this)
        this.browse_button.setGeometry(QtCore.QRect(10, 10, 110, 35))
        this.browse_button.clicked.connect(this.browsePressed)

        this.createdir_button = QtGui.QPushButton(this)
        this.createdir_button.setGeometry(QtCore.QRect(125, 10, 110, 35))
        this.createdir_button.clicked.connect(this.createFolderPressed)

        this.logout_button = QtGui.QPushButton(this)
        this.logout_button.setGeometry(QtCore.QRect(420, 460, 50, 30))
        this.logout_button.clicked.connect(this.logoutPressed)


        this.rename_button = QtGui.QPushButton(this)
        this.rename_button.setGeometry(QtCore.QRect(240, 10, 110, 35))

        this.download_button = QtGui.QPushButton(this)
        this.download_button.setGeometry(QtCore.QRect(355, 10, 115, 35))

        this.lineEdit = QtGui.QLineEdit(this)
        this.lineEdit.setGeometry(QtCore.QRect(10, 50, 460, 29))
        this.file_list = QtGui.QListWidget(this)
        this.file_list.setGeometry(QtCore.QRect(10, 90, 460, 320))
        global diricon
        diricon = QtGui.QIcon()
        diricon.addPixmap(QtGui.QPixmap("if_folder_299060.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)

        this.setWindowTitle("Form")
        __sortingEnabled = this.file_list.isSortingEnabled()
        this.file_list.setSortingEnabled(False)
        this.file_list.setSortingEnabled(__sortingEnabled)
        this.file_list.itemDoubleClicked.connect(this.itemClicked)

        this.upload_button.setText("Upload")
        this.browse_button.setText("Browse")
        this.createdir_button.setText("Create Folder")
        this.rename_button.setText("Rename File")
        this.download_button.setText("Download")
        this.logout_button.setText("Logout")
    def addDirectory(this, name):
        global diricon
        global dir
        dir = QtGui.QListWidgetItem(this.file_list)
        dir.setIcon(diricon)
        dir.setText(name+"/")
    def itemClicked(this):
        if this.file_list.selectedItems()[0].text()[-1] == "/":
            this.path += this.file_list.selectedItems()[0].text()
            print this.path
            global client_socket
            client_socket.sendall(pickle.dumps(["showDir", this.path]))
            this.file_list.clear()
            data = pickle.loads(client_socket.recv(4096))
            for x in data:
                if isinstance(x, Directory):
                    this.addDirectory(x.dirName)
                else:
                    this.addFile(x.fileName)
        elif this.file_list.selectedItems()[0].text() == "..":
            if this.path != "./users/" + this.username+"/":
                this.path = this.path[:this.path.rfind("/")]
                this.path = this.path[:this.path.rfind("/")+1]
                client_socket.sendall(pickle.dumps(["showDir", this.path]))
                this.file_list.clear()
                data = pickle.loads(client_socket.recv(4096))
                for x in data:
                    if isinstance(x, Directory):
                        this.addDirectory(x.dirName)
                    else:
                        this.addFile(x.fileName)
    def addFile(this, name):
        file = QtGui.QListWidgetItem(this.file_list)
        file.setText(name)
    def center(this):
        qr = this.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        this.move(qr.topLeft())
    def browsePressed(this):
        this.dialog = QtGui.QFileDialog(this)
        this.dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        if this.dialog.exec_():
            fileName = this.dialog.selectedFiles()
            this.lineEdit.setText(fileName[0])
    def createFolderPressed(this):
        dirName, ok = QtGui.QInputDialog.getText(this, 'Create a folder','Enter folder name:')
        valid = True
        if "." in dirName or "/" in dirName or "\\" in dirName or "?" in dirName or "|" in dirName or "*" in dirName or ":" in dirName or "<" in dirName or ">" in dirName or '"' in dirName:
            valid = False
            QtGui.QMessageBox.critical(None, "Error", 'A folder name can\'t contain any of the following characters:\n \\ / : * ? " < > |')
        exists = False
        if valid == True:
            for x in xrange(this.file_list.count()):
                if this.file_list.item(x).text() == dirName+"/":
                    exists = True
                    QtGui.QMessageBox.critical(None, "Error","A folder with that name already exists.")
                    break
        if ok and not exists and valid:
            global client_socket
            client_socket.sendall(pickle.dumps(["mkDir",this.path+dirName+"/"]))
            data = pickle.loads(client_socket.recv(4096))
            this.file_list.clear()
            for x in data:
                if isinstance(x, Directory):
                    this.addDirectory(x.dirName)
                else:
                    this.addFile(x.fileName)
    def logoutPressed(this):
        global login_ins
        this.close()
        login_ins.center()
        login_ins.show()
main()