import sys,os
from os import path
import sqlite3,time
import datetime
import fnmatch
import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from ui_addNew import Ui_addNew
from ui_update import Ui_update
from ui_delete import Ui_remove
from ui_view import Ui_view
from trainer import trainAll

class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)
    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)
        self.camera.set(3, 640)
        self.camera.set(4, 360)
        self.timer = QtCore.QBasicTimer()
    def start_recording(self):       
        self.timer.start(0, self)
    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return
        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)

class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, haar_cascade_filepath,flag, parent=None):
        super().__init__(parent)
        self.flag=flag
        self.names = {}
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (20, 20)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        connection = sqlite3.connect('myRecogniser.db')
        cur = connection.cursor()
        cur.execute('''SELECT * FROM Person''')
        for u,n,i in cur.fetchall():           
            self.names[u]=n
        try:
            self.recognizer.read('trainer/trainer.yml')
        except:
            QtWidgets.QMessageBox.warning(self,"Error","Some problem with trainer file. Kindly re-train.",QtWidgets.QMessageBox.Ok)
    def readNew(self):
        try:
            self.recognizer.read('trainer/trainer.yml')
        except:
            QtWidgets.QMessageBox.warning(self,"Error","Some problem with trainer file. Kindly re-train.",QtWidgets.QMessageBox.Ok)  
    def detect_faces(self, image: np.ndarray):
        value=[]
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)
        value.append(gray_image)
        faces = self.classifier.detectMultiScale(gray_image,scaleFactor=1.3,minNeighbors=4,flags=cv2.CASCADE_SCALE_IMAGE,minSize=self._min_size)
        value.append(faces)
        return value

    def image_data_slot(self, image_data):   
        font = cv2.FONT_HERSHEY_SIMPLEX
        value1 = self.detect_faces(image_data)
        faces=value1[1]
        gray=value1[0]
        uid = 0
        for (x, y, w, h) in faces:
            if self.flag==0:
                img=cv2.rectangle(image_data,(x, y),(x+w, y+h),self._red,self._width)
                uid, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
                if (confidence > 100):
                    uid = str(uid)
                    name = self.names.get(uid)
                    confidence = "{0} - {1}%".format(name,round(confidence))
                    cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
                else:
                    id = "unknown"
                    cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2) 
        if self.flag==0:
            self.image = self.get_qimage(image_data)
            if self.image.size() != self.size():
                self.setFixedSize(self.image.size())
            self.update()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)
        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

class FaceViewer(QtWidgets.QWidget):
    def __init__(self, haar_cascade_filepath,flag, parent=None):
        super().__init__(parent)
        self.flag=flag
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (20, 20)
        
    def detect_faces(self, image: np.ndarray):
        value=[]
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)
        value.append(gray_image)
        faces = self.classifier.detectMultiScale(gray_image,scaleFactor=1.3,minNeighbors=4,flags=cv2.CASCADE_SCALE_IMAGE,minSize=self._min_size)
        value.append(faces)
        return value

    def image_data_slot(self, image_data):
        font = cv2.FONT_HERSHEY_SIMPLEX
        value1 = self.detect_faces(image_data)
        faces=value1[1]
        gray=value1[0]
        for (x, y, w, h) in faces:
            if self.flag==1 :
                img=cv2.rectangle(image_data,(x, y),(x+w, y+h),self._red,self._width)
        if self.flag==1:
            self.image = self.get_qimage(image_data)
            if self.image.size() != self.size():
                self.setFixedSize(self.image.size())
            self.update()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)
        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()


class MainWidget(QtWidgets.QWidget):

    def openAddNew(self):
        os.execl(sys.executable,'python ui_addNew.py')
        sys.exit()

    def openDelete(self):
        self.deleteDialog = QtWidgets.QDialog()
        self.ui = Ui_remove()
        self.ui.setupUi(self.deleteDialog,self.total,self.totalP)
        self.deleteDialog.show()

    def openUpdate(self):
        os.execl(sys.executable,'python ui_update.py')
        sys.exit()

    def openView(self):
        self.viewDialog = QtWidgets.QDialog()
        self.ui = Ui_view()
        self.ui.setupUi(self.viewDialog)
        self.viewDialog.show()

    def openRecogniser(self):
        self.label_status.setText('Status : finding who are you? ')
        self.btn_rec.setText("Pause..")
        self.btn_rec.clicked.connect(self.pauseRecogniser)
        
        self.innerlayoutT.removeWidget(self.face_viewer)
        self.face_viewer.flag=0
        self.face_detection_widget.flag=0
        self.record_video.image_data.disconnect(self.image_data_slot)       
        self.image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(self.image_data_slot)
        self.record_video.start_recording()
        self.innerlayoutT.addWidget(self.face_detection_widget)

    def pauseRecogniser(self):
        self.label_status.setText('Status : Ideal Recognisiton')
        self.btn_rec.setText("RECOGNIZE")
        self.btn_rec.clicked.connect(self.openRecogniser)
        self.record_video.image_data.disconnect(self.image_data_slot)
        self.face_viewer.flag=1
        self.face_detection_widget.flag=1
        self.innerlayoutT.removeWidget(self.face_detection_widget)
        self.image_data_slot = self.face_viewer.image_data_slot
        self.record_video.image_data.connect(self.image_data_slot)
        self.record_video.start_recording()
        self.innerlayoutT.addWidget(self.face_viewer)

    def openTrainer(self):
        self.label_status.setText('Status : Training.....please wait...')
        time.sleep(1)
        train = trainAll()
        self.face_detection_widget.readNew()
        if train.state >= 1:
            self.label_status.setText('Status : Trained')
            QtWidgets.QMessageBox.information(self,"Success",'Successfully trained {0} faces'.format(train.state),QtWidgets.QMessageBox.Ok)
            self.label_status.setText('Status : Trained {0} persons :) '.format(train.state))
            self.total.setText('Total Registered :{0}'.format(train.state))
        else:
            self.label_status.setText('Status : Failure can\'t train')
            QtWidgets.QMessageBox.information(self,"Error","Some error occured while training... We are sorry.",QtWidgets.QMessageBox.Ok)

    def __init__(self, haarcascade_filepath, parent=None):
        super().__init__(parent)
        layoutL = QtWidgets.QVBoxLayout()
        self.innerlayoutT = QtWidgets.QVBoxLayout()
        self.fp = haarcascade_filepath    
        self.face_viewer = FaceViewer(self.fp,1)
        self.face_detection_widget = FaceDetectionWidget(self.fp,1)
        self.record_video = RecordVideo()
        self.image_data_slot = self.face_viewer.image_data_slot
        self.record_video.image_data.connect(self.image_data_slot)
        self.record_video.start_recording()
        self.innerlayoutT.addWidget(self.face_viewer)
        connection = sqlite3.connect('myRecogniser.db')
        cur = connection.cursor() 
        cur.execute("SELECT * FROM Person")
        result = cur.fetchall()
        self.totalP=len(result)
        innerlayoutB = QtWidgets.QHBoxLayout()
        self.label_status = QtWidgets.QLabel('Status : Ideal Recognisition')
        innerlayoutB.addWidget(self.label_status)
        self.total = QtWidgets.QLabel('Total Registered: {}'.format(self.totalP))
        innerlayoutB.addWidget(self.total)
        layoutL.addLayout(self.innerlayoutT)
        layoutL.addLayout(innerlayoutB)
        layoutR = QtWidgets.QVBoxLayout()
        self.btn_rec = QtWidgets.QPushButton("RECOGNIZE")
        layoutR.addWidget(self.btn_rec)
        self.btn_rec.clicked.connect(self.openRecogniser)
        self.btn_trn = QtWidgets.QPushButton("TRAIN")
        layoutR.addWidget(self.btn_trn)
        self.btn_trn.clicked.connect(self.openTrainer)
        self.btn_add = QtWidgets.QPushButton("ADD NEW")
        layoutR.addWidget(self.btn_add)
        self.btn_add.clicked.connect(self.openAddNew)
        self.btn_delete = QtWidgets.QPushButton("DELETE")
        layoutR.addWidget(self.btn_delete)
        self.btn_delete.clicked.connect(self.openDelete)
        self.btn_update = QtWidgets.QPushButton("UPDATE")
        layoutR.addWidget(self.btn_update)
        self.btn_update.clicked.connect(self.openUpdate)
        self.btn_view = QtWidgets.QPushButton("VIEW")
        layoutR.addWidget(self.btn_view)
        self.btn_view.clicked.connect(self.openView)
        self.btn_quit = QtWidgets.QPushButton("QUIT")
        layoutR.addWidget(self.btn_quit)
        self.btn_quit.clicked.connect(self.close_SSS)
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(layoutL)
        mainLayout.addLayout(layoutR)       
        self.setLayout(mainLayout)

    def close_SSS(self):
        choice = QtWidgets.QMessageBox.question(self,"QuitApp","Are you sure that you want to quit the application?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

def main(haar_cascade_filepath):
    app  = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget(haar_cascade_filepath)
    main_window.setCentralWidget(main_widget)
    main_window.setWindowTitle("Face Recognition")
    main_window.setWindowIcon(QtGui.QIcon('gui/logo.png'))
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    script_dir = path.dirname(path.realpath(__file__))
    cascade_filepath = path.join(script_dir,'.','cascades','haarcascade_frontalface_default.xml')
    cascade_filepath = path.abspath(cascade_filepath)
    main(cascade_filepath)
