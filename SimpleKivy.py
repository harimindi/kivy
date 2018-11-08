from kivy.app import App
from kivy.uix.label import Label
import cv2
import numpy as np
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

class SimpleKivy(App):
    def build(self):

        faceCascade = cv2.CascadeClassifier("C:\Hari Docs\Kivy\haarcascade_frontalfaces_default.xml")

        video_capture = cv2.VideoCapture(0)
        count = 0
        while (count < 40):
            
            ret, frame = video_capture.read()
            print (np.shape(frame))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #gray = frame
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
                
            )

            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            count = count + 1
        
        video_capture.release()
        cv2.destroyAllWindows()
        return Label(text = "Face Detection Application")
        
if __name__=="__main__":
    SimpleKivy().run()
