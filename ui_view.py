
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class Ui_view(QtWidgets.QMainWindow):

    def setupUi(self, view):
        self.view=view
        view.setObjectName("view")
        view.resize(200,130)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        view.setWindowIcon(icon)
        self.index=1
        self.status=1
        self.formLayout = QtWidgets.QFormLayout(view)
        self.formLayout.setObjectName("formLayout")
        self.label_uid = QtWidgets.QLabel(view)
        self.label_uid.setObjectName("label_uid")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_uid)
        self.label_name = QtWidgets.QLabel(view)
        self.label_name.setObjectName("label_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_name)
        self.image_btn = QtWidgets.QPushButton(view)
        self.image_btn.setObjectName("data_view")
        self.image_btn.clicked.connect(self.readData)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.image_btn)
        self.buttonBox = QtWidgets.QDialogButtonBox(view)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.buttonBox)
        self.retranslateUi(view)
        self.buttonBox.accepted.connect(view.accept)
        QtCore.QMetaObject.connectSlotsByName(view)
        
    def retranslateUi(self, view):
        _translate = QtCore.QCoreApplication.translate
        view.setWindowTitle(_translate("view", "View"))
        self.image_btn.setText("View data")
        self.label_name.setText("Name")
        self.label_uid.setText("UID")

    def addRow(self,datau,datan):
        view = self.view
        label_uid = QtWidgets.QLabel(view)
        label_uid.setObjectName("uid")
        self.formLayout.setWidget(self.index, QtWidgets.QFormLayout.LabelRole,label_uid)
        label_uid.setText(datau)
        label_name = QtWidgets.QLabel(view)
        label_name.setObjectName("name")
        self.formLayout.setWidget(self.index, QtWidgets.QFormLayout.FieldRole,label_name)
        label_name.setText(datan)
        self.index +=1

    def readData(self):
        connection = sqlite3.connect('myRecogniser.db')
        cur = connection.cursor() 
        self.status = cur.execute('''SELECT uid,name FROM Person ORDER BY uid asc''')
        self.status = len(cur.fetchall())
        cur.execute('''SELECT * FROM Person order by uid''')
        if self.status == 0:
            connection.close()
            QtWidgets.QMessageBox.warning(self,"Unsuccessfull","No data",QtWidgets.QMessageBox.Ok)
        else:
            self.formLayout.removeWidget(self.image_btn)
            self.image_btn.setVisible(False)
            try:
                for datau,datan,d in cur.fetchall():
                    self.addRow(datau,datan)
            finally:
                connection.close()
                return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    view = QtWidgets.QDialog()
    ui = Ui_view()
    ui.setupUi(view)
    view.show()
    sys.exit(app.exec_())

