import cv2
import os,sqlite3
class registration:
    def __init__(self,uid,name):
        self.uid=uid
        self.name=name
    def registerUser(self):
        try:
            cam = cv2.VideoCapture(0)
            cam.set(3, 640)
            cam.set(4, 360)
            face_detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
            uid=self.uid
            name=self.name
            count = 0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(gray, (x,y), (x+w, y+h), (255,0,0), 2)
                    cv2.imwrite("dataset/User." + str(uid) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                    cv2.imshow('Learning face', gray)
                    if count is 25:
                        connection = sqlite3.connect('myRecogniser.db')
                        cur = connection.cursor()
                        image_path = "dataset/User." + str(uid) + '.' + str(count) + ".jpg"
                        status = cur.execute('''INSERT INTO Person(uid,name,imagePath) VALUES(?,?,?)''',(uid,name,image_path,))
                        connection.commit()
                    count += 1
                k = cv2.waitKey(100) & 0xff
                if k == 27:
                    break
                elif count >= 26:
                    break
        except:
            return 0
        finally:
            cam.release()
            cv2.destroyAllWindows()
            connection.close()
            return 1

    def reregisterUser(self):
        try:
            cam = cv2.VideoCapture(0)
            cam.set(3, 640)
            cam.set(4, 360)
            face_detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
            uid=self.uid
            name=self.name
            count = 0
            for i in range(0,26):
                fpath = "dataset/User.{0}.{1}.jpg".format(uid,i)
                os.remove(fpath)
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(gray, (x,y), (x+w, y+h), (255,0,0), 2)
                    cv2.imwrite("dataset/User." + str(uid) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                    cv2.imshow('Learning face', gray)
                    if count is 25:
                        connection = sqlite3.connect('myRecogniser.db')
                        cur = connection.cursor()
                        image_path = "dataset/User." + str(uid) + '.' + str(count) + ".jpg"
                        status = cur.execute('''UPDATE Person SET name=?,imagePath=? where uid=?''',(name,image_path,uid,))
                        connection.commit()
                    count += 1
                k = cv2.waitKey(100) & 0xff
                if k == 27:
                    break
                elif count >= 26:
                    break
        except:
            return 0
        finally:
            cam.release()
            cv2.destroyAllWindows()
            connection.close()
            return 1
if __name__ == "__main__":   
    reg = registration(101,'default')
    reg.registerUser()
