from PySide import QtCore, QtGui

class Upload(object):
    def setupUi(this, Form):
        Form.setObjectName("Form")
        Form.resize(450, 475)
        
        this.file_list = QtGui.QListWidget(Form)
        this.file_list.setGeometry(QtCore.QRect(10, 80, 421, 321))
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../archlinux-512.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        item = QtGui.QListWidgetItem(this.file_list)
        item.setIcon(icon)
        QtGui.QListWidgetItem(this.file_list)
        QtGui.QListWidgetItem(this.file_list)
        QtGui.QListWidgetItem(this.file_list)
        QtGui.QListWidgetItem(this.file_list)
        
        this.progressBar = QtGui.QProgressBar(Form)
        this.progressBar.setGeometry(QtCore.QRect(20, 400, 401, 31))
        this.progressBar.setProperty("value", 0)
        
        this.upload_button = QtGui.QPushButton(Form)
        this.upload_button.setGeometry(QtCore.QRect(180, 430, 85, 35))
        
        this.browse_button = QtGui.QPushButton(Form)
        this.browse_button.setGeometry(QtCore.QRect(10, 10, 100, 35))
        
        this.createdir_button = QtGui.QPushButton(Form)
        this.createdir_button.setGeometry(QtCore.QRect(120, 10, 100, 35))
        
        this.lineEdit = QtGui.QLineEdit(Form)
        this.lineEdit.setGeometry(QtCore.QRect(10, 50, 411, 29))
        
        this.rename_button = QtGui.QPushButton(Form)
        this.rename_button.setGeometry(QtCore.QRect(230, 10, 100, 35))
        
        this.download_button = QtGui.QPushButton(Form)
        this.download_button.setGeometry(QtCore.QRect(340, 10, 85, 35))
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = this.file_list.isSortingEnabled()
        this.file_list.setSortingEnabled(False)
        this.file_list.item(0).setText(QtGui.QApplication.translate("Form", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        this.file_list.item(1).setText(QtGui.QApplication.translate("Form", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        this.file_list.item(2).setText(QtGui.QApplication.translate("Form", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        this.file_list.item(3).setText(QtGui.QApplication.translate("Form", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        this.file_list.item(4).setText(QtGui.QApplication.translate("Form", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        
        this.file_list.setSortingEnabled(__sortingEnabled)
        this.upload_button.setText(QtGui.QApplication.translate("Form", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        this.browse_button.setText(QtGui.QApplication.translate("Form", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        this.createdir_button.setText(QtGui.QApplication.translate("Form", "Create Folder", None, QtGui.QApplication.UnicodeUTF8))
        this.rename_button.setText(QtGui.QApplication.translate("Form", "Rename File", None, QtGui.QApplication.UnicodeUTF8))
        this.download_button.setText(QtGui.QApplication.translate("Form", "Download", None, QtGui.QApplication.UnicodeUTF8))

