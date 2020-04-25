from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3,os

class Ui_remove(QtWidgets.QMainWindow):
    def setupUi(self, remove, label,lblval):
        self.label = label
        self.lblval = lblval
        remove.setObjectName("remove")
        remove.resize(200, 130)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        remove.setWindowIcon(icon)
        self.status = 0
        self.formLayout = QtWidgets.QFormLayout(remove)
        self.formLayout.setObjectName("formLayout")
        self.uid = QtWidgets.QLineEdit(remove)
        self.uid.setObjectName("uid")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.uid)
        self.label_uid = QtWidgets.QLabel(remove)
        self.label_uid.setObjectName("label_uid")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_uid)
        self.image_btn = QtWidgets.QPushButton(remove)
        self.image_btn.setObjectName("image_btn")
        self.image_btn.clicked.connect(self.deleteData)
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.image_btn)
        self.label_suc = QtWidgets.QLabel(remove)
        self.label_suc.setObjectName("label_suc")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.label_suc)
        self.buttonBox = QtWidgets.QDialogButtonBox(remove)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.FieldRole, self.buttonBox)
        self.retranslateUi(remove)
        self.buttonBox.accepted.connect(remove.accept)
        self.buttonBox.rejected.connect(remove.reject)
        QtCore.QMetaObject.connectSlotsByName(remove)
        self.buttonBox.accepted.connect(self.nothing)

    
    def nothing(self):
        if self.status == 0:
            QtWidgets.QMessageBox.information(self,"Message","You provide nothing to delete",QtWidgets.QMessageBox.Ok)

    def retranslateUi(self, remove):
        _translate = QtCore.QCoreApplication.translate
        remove.setWindowTitle(_translate("remove", "Delete"))
        self.label_uid.setText(_translate("remove", "Enter UID"))
        self.image_btn.setText(_translate("addNew", "Delete face data"))


    def deleteData(self):
        uid = self.uid.text()
        if uid == "":
            QtWidgets.QMessageBox.warning(self,"Warning","Can't delete face data. Please fill all the fields.",QtWidgets.QMessageBox.Ok)
        else:
            self.status = self.deleteUser()
        if self.status:
            self.label_suc.setText("Success")
        else:
            self.label_suc.setText("Failure")
        
    def deleteUser(self):       
        connection = sqlite3.connect('myRecogniser.db')
        cur = connection.cursor() 
        uid = self.uid.text()
        cur.execute('''DELETE FROM Person WHERE uid=?''',(uid,))
        check=cur.rowcount
        if check is 1:
            connection.commit()
            connection.close()
            for i in range(0,26):
                fpath = "dataset/User.{0}.{1}.jpg".format(uid,i)
                os.remove(fpath)
            QtWidgets.QMessageBox.information(self,"Successfull","You have successfully deleted a person with UID {}".format(uid),QtWidgets.QMessageBox.Ok)
            self.label.setText('Total Registered :{0}'.format(self.lblval-1))

            return 1
        else:
            connection.close()
            QtWidgets.QMessageBox.warning(self,"Unsuccessfull","No such person found",QtWidgets.QMessageBox.Ok)
            return 0

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    remove = QtWidgets.QDialog()
    ui = Ui_remove()
    ui.setupUi(remove)
    remove.show()
    sys.exit(app.exec_())

