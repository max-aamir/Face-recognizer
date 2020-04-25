from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3,cv2,os,sys
import dataset

class Ui_addNew(QtWidgets.QMainWindow):
    def setupUi(self, addNew):      
        addNew.setObjectName("addNew")
        addNew.resize(200,130)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        addNew.setWindowIcon(icon)   
        self.status = 0
        self.formLayout = QtWidgets.QFormLayout(addNew)
        self.formLayout.setObjectName("formLayout")
        self.label_name = QtWidgets.QLabel(addNew)
        self.label_name.setObjectName("label_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_name)
        self.name = QtWidgets.QLineEdit(addNew)
        self.name.setObjectName("name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name)
        self.uid = QtWidgets.QLineEdit(addNew)
        self.uid.setObjectName("uid")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.uid)
        self.label_uid = QtWidgets.QLabel(addNew)
        self.label_uid.setObjectName("label_uid")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_uid)
        self.image_btn = QtWidgets.QPushButton(addNew)
        self.image_btn.setObjectName("image_btn")
        self.image_btn.clicked.connect(self.openImage)
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.image_btn)
        self.label_suc = QtWidgets.QLabel(addNew)
        self.label_suc.setObjectName("label_uid")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.label_suc)
        self.buttonBox = QtWidgets.QDialogButtonBox(addNew)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.FieldRole, self.buttonBox)
        self.retranslateUi(addNew)
        self.buttonBox.accepted.connect(addNew.accept)
        self.buttonBox.rejected.connect(addNew.reject)
        QtCore.QMetaObject.connectSlotsByName(addNew)
        self.buttonBox.accepted.connect(self.nothing)
        self.buttonBox.rejected.connect(self.nothing2)
  
    def nothing2(self):
        os.execl(sys.executable,'python gui.py')
    def nothing(self):
        if self.status == 0:
            QtWidgets.QMessageBox.information(self,"Message","You provide nothing to add",QtWidgets.QMessageBox.Ok)
        os.execl(sys.executable,'python gui.py')
    def retranslateUi(self, addNew):
        _translate = QtCore.QCoreApplication.translate
        addNew.setWindowTitle(_translate("addNew", "Add New User"))
        self.label_name.setText(_translate("addNew", "Name"))
        self.label_uid.setText(_translate("addNew", "UID"))
        self.image_btn.setText(_translate("addNew", "Add face data"))

    def openImage(self):
        uid = self.uid.text()
        name = self.name.text()
        if uid == "" or name == "":
            QtWidgets.QMessageBox.warning(self,"Warning","Can't add face data. Please fill all the fields.",QtWidgets.QMessageBox.Ok)
        else:
            register = dataset.registration(uid,name)
            self.status = register.registerUser()
        if self.status:
            self.label_suc.setText("Success")
        else:
            self.label_suc.setText("Failure")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addNew = QtWidgets.QDialog()
    ui = Ui_addNew()
    ui.setupUi(addNew)
    addNew.show()
    sys.exit(app.exec_())