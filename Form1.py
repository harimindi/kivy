#Import for Blink Detection
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream, FPS, VideoStream
from imutils import face_utils
import imutils
import argparse
import numpy as np
import time
import dlib
import cv2
#Imports for Kivy UI
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
#from kivy.uix.label import Label
#from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from KivyCalendar import DatePicker
from kivy.uix.screenmanager import ScreenManager, Screen


class MainScreen(Screen):
    #from kivy.properties import ObjectProperty
    #theTxt = ObjectProperty(None)
    pass
    '''
    def build(self):
        kivy = Builder.load_file('Form1.kv')
        return kivy
    
    def show_calendar(self):
        datePicker = CustomDatePicker()
        datePicker.show_popup(1, .3)
    '''    
class IDScreen(Screen):
    def onCameraClick(self, *args):
        image = self.ids['img']
        
        def eye_aspect_ratio(eye):
            A = dist.euclidean(eye[1], eye[5])
            B = dist.euclidean(eye[2], eye[4])
            C = dist.euclidean(eye[0], eye[3])
            ear = (A + B) / (2.0 * C)
            return ear
        
        EYE_AR_THRESH = 0.3
        EYE_AR_CONSEC_FRAMES = 3
         
        # initialize the frame counters and the total number of blinks
        COUNTER = 0
        TOTAL = 1
        
        shape_predictor = 'F:/Data_Science/FaceRecognition/shape_predictor_68_face_landmarks.dat'
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(shape_predictor)
        
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
        
        print("[INFO] starting video stream thread...")
        vs = VideoStream(src=0).start()
        fileStream = False
        time.sleep(1.0)
        cv2.namedWindow('Capture', cv2.WINDOW_NORMAL)
        flag = 1
        while (flag == 1):
            frame = vs.read()
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
            rects = detector(gray, 0)
            
            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
         
                ear = (leftEAR + rightEAR) / 2.0
                
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                
                if ear < EYE_AR_THRESH:
                    COUNTER += 1
                else:
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        print('Blink detected, stay steady and look at the camera...!')
                        frame = vs.read()
                        time.sleep(5) 
                        img_name =  'opencv_frame_{}.png'.format(TOTAL)
                        cv2.imwrite(img_name, frame)    
                        print('{} written'.format(img_name))
                        flag = 0                        
                    COUNTER = 0  # reset the eye frame counter
            cv2.imshow('Capture', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        vs.stop()
        cv2.destroyAllWindows()               
        image.source = img_name


class ScreenManagement(ScreenManager):
    pass

'''
class CustomDatePicker(DatePicker):

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = "%s.%s.%s" % tuple(self.cal.active_date)
        self.focus = False
        App.get_running_app().root.ids.txt_DOB.text = self.text
'''
kivy = Builder.load_file("Form1.kv")
class Form1(App):
    def build(self):
        return kivy
if __name__=='__main__':
    Form1().run()
