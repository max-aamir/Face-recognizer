from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3,os
import dataset

class Ui_update(QtWidgets.QMainWindow):
    def setupUi(self, update):
        update.setObjectName("update")
        update.resize(200, 130)
        self.status = 0
        self.named = ""
        self.formLayout = QtWidgets.QFormLayout(update)
        self.formLayout.setObjectName("formLayout")
        self.uid = QtWidgets.QLineEdit(update)
        self.uid.setObjectName("uid")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.uid)
        self.label_uid = QtWidgets.QLabel(update)
        self.label_uid.setObjectName("label_uid")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_uid)
        self.btn_record = QtWidgets.QPushButton(update)
        self.btn_record.setObjectName("btn_record")
        self.btn_record.clicked.connect(self.getRecord)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.btn_record)        
        self.buttonBox = QtWidgets.QDialogButtonBox(update)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(16, QtWidgets.QFormLayout.FieldRole, self.buttonBox)
        self.retranslateUi(update)
        self.buttonBox.accepted.connect(update.accept)
        self.buttonBox.rejected.connect(update.reject)
        QtCore.QMetaObject.connectSlotsByName(update)
        self.buttonBox.accepted.connect(self.nothing)
        self.buttonBox.rejected.connect(self.nothing2)

    
    def nothing2(self):
        os.execl(sys.executable,'python gui.py')
    def nothing(self):
        if self.status == 0:
            QtWidgets.QMessageBox.information(self,"Message","Nothing updated",QtWidgets.QMessageBox.Ok)
        os.execl(sys.executable,'python gui.py')

    def retranslateUi(self, update):
        _translate = QtCore.QCoreApplication.translate
        update.setWindowTitle(_translate("update", "Update"))
        self.label_uid.setText(_translate("delete", "UID"))
        self.btn_record.setText(_translate("delete", "Check Record"))
        
    def addUI(self,update):    
        self.label_name = QtWidgets.QLabel(update)
        self.label_name.setObjectName("label_name")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_name)
        self.label_name.setText("Name")
        self.uid.setReadOnly(True)
        self.btn_record.setEnabled(False)
        self.name = QtWidgets.QLineEdit(update)
        self.name.setObjectName("name")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.name)
        self.name.setText(self.named)
        self.label_suc = QtWidgets.QLabel(update)
        self.label_suc.setObjectName("label_suc")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.label_suc)
        self.image_btn = QtWidgets.QPushButton(update)
        self.image_btn.setObjectName("image_btn")
        self.image_btn.clicked.connect(self.openImage)
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.image_btn)
        self.image_btn.setText("Update face data")

    def getRecord(self):
        uid = self.uid.text()
        if uid == "":
            QtWidgets.QMessageBox.warning(self,"Error","Sorry, Please enter UID",
                QtWidgets.QMessageBox.Ok)
        else:
            connection = sqlite3.connect('myRecogniser.db')
            cur = connection.cursor()
            status = cur.execute('''select * from Person where uid=?''',(uid,))
            if status:
                u,n,i = cur.fetchone()
                self.named = n
                self.addUI(update)
            else:
                QtWidgets.QMessageBox.warning(self,"Can\'t Update","No person with UID : {0} found".format(uid),
                    QtWidgets.QMessageBox.Ok)
            connection.close()

    def openImage(self):
        uid = self.uid.text()
        name = self.name.text()
        if uid == "" or name == "":
            QtWidgets.QMessageBox.warning(self,"Warning","Can't add face data. Please fill all the fields.",QtWidgets.QMessageBox.Ok)
        else:
            register = dataset.registration(uid,name)
            self.status = register.reregisterUser()
        if self.status:
            self.label_suc.setText("Success")
        else:
            self.label_suc.setText("Failure")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    update = QtWidgets.QDialog()
    ui = Ui_update()
    ui.setupUi(update)
    update.show()
    sys.exit(app.exec_())

